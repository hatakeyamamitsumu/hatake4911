
import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLOWorld  # YOLOv8ライブラリをインポート

# モデルの読み込み (モデルのパスは適宜変更)
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt') # モデルのパスを適宜変更

# セッション状態を初期化
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None

# カメラ入力
picture = st.camera_input("写真を撮ってください")

if picture:
    # OpenCVで画像を読み込む
    byte_arr = np.frombuffer(picture.read(), np.uint8)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    # セッション状態に画像を保存
    st.session_state.captured_image = cv_image

    # 画像を表示
    st.image(cv_image, channels="BGR")

# セッション状態に画像がある場合、YOLOで分析するボタンを表示
if st.session_state.captured_image is not None:
    if st.button("画像を分析"):
        # YOLOで物体検出
        results = model(st.session_state.captured_image[None, ...])
        # 結果を可視化
        result_img = results[0].plot()
        st.image(result_img, channels="RGB")
