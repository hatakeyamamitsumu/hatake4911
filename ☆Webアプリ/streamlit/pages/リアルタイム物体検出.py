import streamlit as st
import cv2
import numpy as np

# Streamlitアプリケーションの設定
st.title('リアルタイム物体検出アプリ')
st.write('PCカメラの映像を使用してリアルタイムで物体検出を行います。')

run = st.checkbox('物体検出を開始')
FRAME_WINDOW = st.image([])

# Webカメラの設定
cap = cv2.VideoCapture(0)

# OpenCVの顔検出器をロード
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while run:
    ret, frame = cap.read()
    if not ret:
        st.error("カメラの映像を取得できませんでした。")
        break

    # グレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顔検出
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 検出された顔に枠を描画
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # フレームを表示
    FRAME_WINDOW.image(frame, channels='BGR')

cap.release()
