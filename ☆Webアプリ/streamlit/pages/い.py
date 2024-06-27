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
    return faces

st.title("顔認識アプリ")
st.write("jpg画像をアップロードしてください。")

# ぼかし具合を選択するスライダー
blur_strength = st.slider('ぼかし具合を選択してください (カーネルサイズ)', 1, 50, 21, step=2)

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file)
    # OpenCV形式に変換
    image_np = np.array(image)
    # 顔認識を実行
    faces = detect_faces(image_np)
    
    if faces:
        st.write("検出された顔:")
        # 各顔に対してぼかしを適用するかどうかを選択するチェックボックス
        for i, face in enumerate(faces):
            x, y, width, height = face['box']
            if st.checkbox(f"顔 {i+1} (信頼度: {face['confidence']:.2f})", key=f"face_{i}"):
                image_np[y:y + height, x:x + width] = cv2.GaussianBlur(image_np[y:y + height, x:x + width], (blur_strength, blur_strength), 0)
            # 検出された顔に矩形を描画
            cv2.rectangle(image_np, (x, y), (x + width, y + height), (255, 0, 0), 2)
    
    # 結果の画像を表示
    st.image(image_np, caption="認識結果", use_column_width=True)
