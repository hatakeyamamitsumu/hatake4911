import streamlit as st
import cv2
import numpy as np

# カメラ入力
picture = st.camera_input("写真を撮ってください")

if picture:
    # OpenCVで画像を読み込む
    byte_arr = np.frombuffer(picture.read(), np.uint8)
    cv_image = cv2.imdecode(byte_arr, cv2.IMREAD_COLOR)

    # 画像を表示
    st.image(cv_image, channels="BGR")

    # 画像を保存し、ダウンロードボタンを表示
    cv2.imwrite("captured_image.jpg", cv_image)
    with open("captured_image.jpg", "rb") as file:
        st.download_button(
            label="画像をダウンロード",
            data=file,
            file_name="captured_image.jpg",
            mime="image/jpeg"
        )
