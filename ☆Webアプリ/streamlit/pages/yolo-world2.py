import streamlit as st
from ultralytics import YOLOWorld
import cv2

# YOLO-Worldモデルの読み込み
model = YOLOWorld('yolov8s.pt')

# 動画ファイルのアップロード
uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mov'])

# 動画ファイルが選択された場合
if uploaded_file is not None:
    # OpenCVで動画を読み込む
    cap = cv2.VideoCapture(uploaded_file)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 物体検出の実行
        results = model.predict(source=frame)

        # 結果の描画 (OpenCVで描画)
        annotated_frame = results[0].plot()

        # Streamlitで画像を表示
        st.image(annotated_frame, channels="BGR")

# 静止画のアップロード
uploaded_image = st.file_uploader("Choose an image file", type=['jpg', 'png'])
if uploaded_image is not None:
    # OpenCVで画像を読み込む
    img = cv2.imread(uploaded_image)

    # 物体検出の実行
    results = model.predict(source=img)

    # 結果の描画 (OpenCVで描画)
    annotated_img = results[0].plot()

    # Streamlitで画像を表示
    st.image(annotated_img, channels="BGR")
