import streamlit as st
from ultralytics import YOLOWorld
import cv2

# 　YOLO-Worldモデルの読み込み
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt')

# PCカメラのキャプチャ
cap = cv2.VideoCapture(0)

# Streamlitのメインパネル
st.title("リアルタイム物体検出 (YOLO-World)")

# 動画を表示する領域
placeholder = st.empty()

# フレームを順次表示
while True:
    # カメラから1フレーム取得
    ret, frame = cap.read()
    if not ret:
        break

    # 物体検出
    results = model.predict(source=frame, conf=0.5, iou=0.45)
    annotated_frame = results[0].plot()

    # OpenCVの画像をRGBに変換
    img_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

    # Streamlitに表示
    placeholder.image(img_rgb, channels="RGB", use_column_width=True)

# 後処理
cap.release()
