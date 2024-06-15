import streamlit as st
import cv2
import numpy as np
import torch
from torchvision import transforms
from PIL import Image

# YOLOv5モデルのロード
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Streamlitアプリケーションの設定
st.title('物体検出アプリ')
st.write('YOLOv5を使用して物体検出を行います。')

# 画像のアップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を読み込む
    image = Image.open(uploaded_file)
    st.image(image, caption='アップロードされた画像', use_column_width=True)
    st.write("")
    st.write("物体検出中...")

    # 画像をnumpy配列に変換
    image_np = np.array(image)

    # 画像をYOLOv5モデルに入力する形式に変換
    results = model(image_np)

    # 検出結果をプロット
    results.render()

    # 検出結果の画像を取得
    detected_image = results.imgs[0]

    # PIL形式に変換して表示
    detected_image = Image.fromarray(detected_image)
    st.image(detected_image, caption='検出結果', use_column_width=True)

    # 検出されたオブジェクトのラベルと信頼度を表示
    st.write("検出されたオブジェクト:")
    for *box, conf, cls in results.xyxy[0]:  # xyxy座標、信頼度、クラスラベル
        st.write(f"{model.names[int(cls)]} (信頼度: {conf:.2f})")

