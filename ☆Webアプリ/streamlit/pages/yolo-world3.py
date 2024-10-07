import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np

# モデルの読み込み (パスを適宜変更)
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt')

# カメラキャプチャの設定
cap = cv2.VideoCapture(0)

def detect_objects(img, model):
    """
    物体検出を行う関数

    Args:
        img: 入力画像
        model: YOLOv8モデル

    Returns:
        処理済みの画像 (BGR形式)
    """

    results = model.predict(source=img)
    annotated_img = results[0].plot()
    return annotated_img

# Streamlitアプリのレイアウト
st.title("YOLOv8 物体検出アプリ")

# カメラ撮影ボタン
if st.button('写真を撮る'):
    ret, frame = cap.read()
    if not ret:
        st.error('カメラから画像を取得できませんでした')
    else:
        # 物体検出
        annotated_frame = detect_objects(frame, model)

        # BGRをRGBに変換
        rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

        # Streamlitに表示
        st.image(rgb_image, channels="RGB", use_column_width=True)

# カメラの解放
cap.release()
