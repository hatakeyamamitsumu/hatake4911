import streamlit as st
import numpy as np
from PIL import Image
import cv2
from mtcnn import MTCNN

# MTCNNの顔検出器を読み込む
detector = MTCNN()

def detect_faces(image):
    # 顔を検出
    faces = detector.detect_faces(image)
    # 検出された顔に矩形を描画
    for face in faces:
        x, y, width, height = face['box']
        cv2.rectangle(image, (x, y), (x + width, y + height), (255, 0, 0), 2)
    return image

st.title("顔認識アプリ")
st.write("jpg画像をアップロードしてください。")

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file)
    # OpenCV形式に変換
    image = np.array(image)
    # 顔認識を実行
    result_image = detect_faces(image)
    # 結果の画像を表示
    st.image(result_image, caption="認識結果", use_column_width=True)
