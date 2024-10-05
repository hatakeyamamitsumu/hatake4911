import streamlit as st
import cv2
import numpy as np  # NumPyモジュールのインポートを追加

# カメラ入力
picture = st.camera_input("Take a picture")

if picture:
    # OpenCVで画像を読み込む
    byte_arr = np.frombuffer(picture.read(), np.uint8)
    cv_image = cv2.imdecode(byte_arr, cv2.IMREAD_COLOR)

    # 画像を表示
    st.image(cv_image, channels="BGR")
