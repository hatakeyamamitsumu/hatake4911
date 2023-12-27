import os

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import cv2
from skimage import morphology
from skimage.measure import label
from skimage.morphology import disk, opening


def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

# 1の処理
def calc_length(img_gray):
    upper_list=[]
    lower_list=[]
    length_list=[]
    for i in range(img_gray.shape[1]):
        particle_index = np.where(img_gray[:,i]==False)[0]
        upper_list.append(particle_index.min())
        lower_list.append(particle_index.max())
        length_list.append(particle_index.max() - particle_index.min())
    return upper_list,lower_list,length_list

# 2の処理
def process_2(img_gray, th=10000):
    return morphology.remove_small_holes(img_gray, area_threshold=th)

# 3の処理
def process_3(img_gray):
    label_image=label(img_gray==False, connectivity=1)

    max_label=1
    max_area=0
    for i in range(1,label_image.max()+1):
        area=(label_image==i).sum()
        if max_area<area:
            max_label=i
            max_area=area

    return label_image!=max_label

# 4の処理
def process_4(img_gray,radius=20):
    footprint = disk(radius=radius)
    opened = opening(img_gray, footprint)
    return opened

# 描画処理
def plot_result(img, upper, lower):
    for i in range(len(upper)):
        cv2.drawMarker(img, (i,upper[i]), (0, 0, 255), markerSize=10, thickness=10, markerType=cv2.MARKER_SQUARE)
        cv2.drawMarker(img, (i,lower[i]), (0, 0, 255), markerSize=10, thickness=10, markerType=cv2.MARKER_SQUARE)

def make_table(length, name, col):
    df = pd.DataFrame()
    df[f'{name}']=[np.mean(length), np.median(length), np.std(length)]
    df.index=['mean','median','std']
    col.dataframe(df)

def main():
    os.makedirs('./data', exist_ok=True)
    st.set_page_config(page_icon="📷", page_title="層厚計測アプリ")

    with st.sidebar:
        radio = st.radio(
            "Choose a method",
            ("process 1", "process 2", "process 3", "process 4")
        )

    with st.sidebar:
        th_2 = st.number_input('process_2_param: 0~100000', 0, 100000, 10000)
        st.write("process_2_param", th_2)

    with st.sidebar:
        th_4 = st.number_input('process_4_param: 0~50', 0, 50, 10)
        st.write("process_4_param", th_4)

    st.title('層厚計測アプリ')

    # アップローダー
    uploaded_image=st.file_uploader("以下からファイルアップロード", type=['jpg','png'])
    # カラム設定
    col1, col2 = st.columns(2)

    col1.header("Original image")
    col2.header("Extracted layer image")

    # original画像表示、2値化処理
    with col1:
        if uploaded_image is not None:
            image=Image.open(uploaded_image,)
            img_array = np.array(image)
            st.image(img_array,use_column_width = None)
            img=pil2cv(image) 
            img_bool = img==255

    # binary画像表示、保存
    if radio=="process 1" and uploaded_image is not None:
        upper_1, lower_1, length_1=calc_length(img_bool)

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        plot_result(img,upper_1,lower_1)

        col2.image(img, channels='BGR')
        make_table(length_1,'process 1', col2)

        cv2.imwrite('./data/image.png', img)
    if radio=="process 2" and uploaded_image is not None:
        img_2 = process_2(img_bool, th=th_2)
        upper_2, lower_2, length_2=calc_length(img_2)

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        plot_result(img,upper_2,lower_2)

        col2.image(img, channels='BGR')
        make_table(length_2,'process 2', col2)

        cv2.imwrite('./data/image.png', img)
    if radio=="process 3" and uploaded_image is not None:
        img_3 = process_3(img_bool)
        upper_3, lower_3, length_3=calc_length(img_3)

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        plot_result(img,upper_3,lower_3)
        make_table(length_3,'process 3', col2)

        col2.image(img, channels='BGR')

        cv2.imwrite('./data/image.png', img)
    if radio=="process 4" and uploaded_image is not None:
        img_4_tmp = process_4(img_bool, radius=th_4)
        img_4 = process_3(img_4_tmp)
        upper_4, lower_4, length_4=calc_length(img_4)

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        plot_result(img,upper_4,lower_4)

        col2.image(img, channels='BGR')
        make_table(length_4,'process 4', col2)

        cv2.imwrite('./data/image.png', img)

    # ダウンロードボタン作成
    if uploaded_image is not None:
        col2.download_button('Download',
            open('./data/image.png', 'br'),
            file_name='image.png')


if __name__ == '__main__':
    main()
