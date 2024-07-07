import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

# YOLOv8モデルの読み込み
model = YOLO('yolov8n.pt')  # yolov8n.ptはYOLOv8の公式プリトレインモデルです

# Streamlitアプリケーションの設定
st.title('リアルタイム物体検出アプリ')
st.write('PCカメラの映像を使用してリアルタイムで物体検出を行います。')

run = st.checkbox('物体検出を開始')
FRAME_WINDOW = st.image([])

# Webカメラの設定
cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        st.error("カメラの映像を取得できませんでした。")
        break

    # 物体検出
    results = model(frame)

    # 検出結果をプロット
    for result in results:
        boxes = result.boxes  # 検出されたボックス
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            class_id = int(box.cls[0])
            label = f"{model.names[class_id]}: {confidence:.2f}"
            
            # 赤枠で囲む
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            y = y1 - 10 if y1 - 10 > 10 else y1 + 10
            cv2.putText(frame, label, (x1, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # フレームを表示
    FRAME_WINDOW.image(frame, channels='BGR')

cap.release()
