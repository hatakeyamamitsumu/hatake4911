import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np

# Model load
model = YOLO("/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8n-pose.pt")  # 姿勢推定モデル

# Title
st.title("YOLOによる姿勢推定アプリ")

# Image upload
uploaded_file = st.file_uploader("画像を選択してください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    try:
        # Image reading
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Inference
        results = model(img)

        # Display results (assuming results.imgs holds images)
        for img in results.imgs:
            st.image(img)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")  
