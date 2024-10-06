import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np

# モデルの読み込み
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt')  # モデルのパスを適宜変更

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
st.title("YOLOv8 物体検出アプリ")

# カメラの使用を選択
use_camera = st.checkbox("カメラを使用する")

# 撮影した画像を保持する変数
captured_image = None

if use_camera:
    # カメラキャプチャ
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("カメラが開けません")
    else:
        # 撮影ボタン
        if st.button('写真を撮る'):
            ret, frame = cap.read()
            if not ret:
                st.error("カメラから画像を取得できませんでした。")
            else:
                # 撮影した画像を保持
                captured_image = frame.copy()
                # 物体検出
                result_img = detect_objects(captured_image, model)
                # 結果を表示
                if result_img is not None:
                    rgb_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                    st.image(rgb_img, channels="RGB", use_column_width=True)
        cap.release()

# 撮影した画像がある場合、再度物体検出ボタンを表示
if captured_image is not None:
    if st.button('再度検出'):
        # 物体検出
        result_img = detect_objects(captured_image, model)
        # 結果を表示
        if result_img is not None:
            rgb_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            st.image(rgb_img, channels="RGB", use_column_width=True)

# 画像アップロードの機能は省略（必要であれば追加）
