import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np

# モデルの読み込み (パスを適宜変更)
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt')

def detect_objects(frame, model):
    """
    物体検出を行う関数

    Args:
        frame: カメラキャプチャのフレーム
        model: YOLOv8モデル

    Returns:
        処理済みの画像 (BGR形式)
    """

    results = model.predict(source=frame)
    annotated_frame = results[0].plot()
    return annotated_frame

# Streamlitアプリのレイアウト
st.title("YOLOv8 物体検出アプリ (PCカメラ)")

# カメラキャプチャの設定
cap = cv2.VideoCapture(0)

# Streamlitの動画表示
placeholder = st.empty()

# リアルタイム処理ループ
while True:
    # フレーム取得
    ret, frame = cap.read()
    if not ret:
        break

    # 物体検出
    annotated_frame = detect_objects(frame, model)

    # BGRをRGBに変換
    rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

    # Streamlitに表示
    placeholder.image(rgb_image, channels="RGB", use_column_width=True)

# 終了処理
cap.release()
