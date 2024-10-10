


import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np

# モデルのロード
model = YOLO("/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolo11n-pose.pt")  # 姿勢推定モデル

# タイトル設定
st.title("YOLOによる姿勢推定アプリ")

# 画像アップロード
uploaded_file = st.file_uploader("画像を選択してください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    try:
        # 画像の読み込み
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # 推論実行
        results = model(img)

        # 推論結果の可視化 (例)
        # results.print()  # 推論結果の詳細を表示
        # results.show()  # 画像上に結果を可視化

        # Streamlitで表示
        st.image(results.imgs[0])
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
