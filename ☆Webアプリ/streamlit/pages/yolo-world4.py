import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np

# モデルの読み込み
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt')

# カメラキャプチャ
cap = cv2.VideoCapture(0)

def detect_objects(img, model, conf_thres=0.5):
    """物体検出を行う関数"""
    try:
        results = model(img[None, ...], conf=conf_thres)
        annotated_img = results[0].plot()
        return annotated_img
    except Exception as e:
        st.error(f"物体検出中にエラーが発生しました: {e}")
        return None

# Streamlitアプリのレイアウト
st.title("YOLOv8 物体検出アプリ (PCカメラ)")

# 信頼度閾値のスライダー
confidence_threshold = st.slider("信頼度閾値", min_value=0.0, max_value=1.0, value=0.5)

placeholder = st.empty()

# 撮影ボタン
if st.button('写真を撮る'):
    ret, frame = cap.read()
    if not ret:
        st.error("カメラから画像を取得できませんでした。")
    else:
        # 物体検出
        result_img = detect_objects(frame, model, confidence_threshold)

        # 結果を表示
        if result_img is not None:
            rgb_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            placeholder.image(rgb_img, channels="RGB", use_column_width=True)

# カメラの解放
cap.release()
