import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np

# モデルの読み込み
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt') # モデルのパスを適宜変更

# 　カメラキャプチャ
cap = cv2.VideoCapture(0)

def detect_objects(img, model, conf_thres=0.5):
    # 物体検出 (バッチサイズ1で処理)
    results = model(img[None, ...], conf=conf_thres)  # 信頼度閾値を設定
    # 検出結果を画像に重ねる
    annotated_img = results[0].plot()
    return annotated_img

# Streamlitアプリのレイアウト
st.title("YOLOv8 物体検出アプリ (PCカメラ)")

# カメラのプレビューを表示する場所
placeholder = st.empty()

# 撮影ボタン
if st.button('写真を撮る'):
    ret, frame = cap.read()
    if not ret:
        st.error("カメラから画像を取得できませんでした。")
    else:
        # 物体検出
        result_img = detect_objects(frame, model)
        # BGRをRGBに変換
        rgb_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        placeholder.image(rgb_img, channels="RGB", use_column_width=True)

# カメラの解放
cap.release()
