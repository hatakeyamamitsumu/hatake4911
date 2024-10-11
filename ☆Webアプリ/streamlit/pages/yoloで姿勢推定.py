import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np

# Model load
#model = YOLO("/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8n-pose.pt")  # 姿勢推定モデル

import streamlit as st
import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np

# モデルの選択
model_options = ["/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8n-pose.pt"]  # ここにモデルを追加
selected_model = st.selectbox("モデルを選択してください", model_options)

# 信頼度閾値の設定
confidence_threshold = st.slider("信頼度閾値", 0.0, 1.0, 0.5)

# 画像または動画のアップロード
uploaded_file = st.file_uploader("画像または動画を選択してください", type=["png", "jpg", "jpeg", "mp4"])

if uploaded_file is not None:
    # モデルのロード
    model = YOLO(selected_model)

    # ファイルの種類によって処理を分岐
    if uploaded_file.type in ["image/png", "image/jpeg"]:
        # 画像処理
        bytes_data = uploaded_file.read()
        np_array = np.frombuffer(bytes_data, np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        results = model(img)
        # ... (画像処理の続き)

    elif uploaded_file.type == "video/mp4":
        # 動画処理
        with st.spinner('動画を処理中です...'):
            # OpenCVで動画を読み込む
            cap = cv2.VideoCapture(uploaded_file)
            # ... (動画処理の続き)

    # 結果の表示
    # matplotlibを使ってグラフや可視化を行う
    # ...

    # 結果の画像をStreamlitに表示
    st.image(annotatedFrame)
