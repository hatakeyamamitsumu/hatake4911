import streamlit as st
import cv2
import numpy as np
from io import BytesIO

def remove_mosaic(img, block_size):
    # モザイク解除を試みる
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
    return img

def main():
    st.title('Mosaic Removal App')

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # アップロードされたファイルを読み込む
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

        # モザイク解除
        block_size = st.slider('Select Mosaic Block Size', min_value=1, max_value=50, value=20)
        denoised_image = remove_mosaic(image, block_size)

        # 元画像とモザイク解除後の画像を表示
        st.image([image, denoised_image], caption=['Original Image', 'Mosaic Removed'], width=300, use_column_width=True)

        # ダウンロードボタンを追加
        if st.button("Download Mosaic Removed Image"):
            # モザイク解除された画像をBytesIOに変換してダウンロード
            denoised_image_io = BytesIO()
            cv2.imwrite(denoised_image_io, cv2.cvtColor(denoised_image, cv2.COLOR_BGR2RGB))
            st.download_button(label="Download", data=denoised_image_io, file_name="mosaic_removed_image.jpg", mime="image/jpeg")

if __name__ == '__main__':
    main()

