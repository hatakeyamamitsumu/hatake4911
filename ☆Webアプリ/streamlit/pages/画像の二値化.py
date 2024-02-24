import cv2
import numpy as np
import streamlit as st
from PIL import Image

def adjust_pixel_color(image, color_adjustment):
    # 二値化された画像を読み込む
    img = cv2.imread(image, cv2.IMREAD_UNCHANGED)

    # 色の調整を行う
    mask = img[:, :] == 0  # 黒い部分（値が0のピクセル）のマスクを作成
    img[mask] = color_adjustment  # 色の調整

    return img

def main():
    st.title('画像2値化アプリ')

    # アップローダー
    uploaded_image = st.file_uploader("以下からファイルアップロード", type=['jpg', 'png'])

    # カラム設定
    col1, col2 = st.columns(2)

    col1.header("Original image")
    col2.header("Colored binary image")

    # original画像表示、2値化処理
    with col1:
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, use_column_width=None)

    # binary画像表示、保存
    if uploaded_image is not None:
        binary_image_path = './data/binary_image.png'
        color_adjustment = (0, 0, 255)  # (B, G, R) 形式のタプル、例: 赤色
        colored_binary_image = adjust_pixel_color(binary_image_path, color_adjustment)
        col2.image(colored_binary_image, channels="BGR")  # BGR チャンネルを表示

if __name__ == '__main__':
    main()
