import streamlit as st
import cv2
import numpy as np

# セッション状態を初期化
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None

# カメラ入力
picture = st.camera_input("写真を撮ってください")

if picture:
    # OpenCVで画像を読み込む
    byte_arr = np.frombuffer(picture.read(), np.uint8)
    cv_image = cv2.imdecode(byte_arr, cv2.IMREAD_COLOR)

    # セッション状態に画像を保存
    st.session_state.captured_image = cv_image

    # 画像を表示
    st.image(cv_image, channels="BGR")

# セッション状態に画像がある場合、表示ボタンを表示
if st.session_state.captured_image is not None:
    if st.button("保存された画像を表示"):
        st.image(st.session_state.captured_image, channels="BGR")
