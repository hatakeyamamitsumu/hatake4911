import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np

# YOLO-Worldモデルの読み込み
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt')

# ファイルアップロード
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # ファイルをNumPy配列に変換
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # 物体検出
    results = model.predict(source=img, conf=0.5, iou=0.45)
    annotated_frame = results[0].plot()

    # OpenCVの画像をRGBに変換
    img_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

    # Streamlitに表示
    st.image(img_rgb, channels="RGB", use_column_width=True)
