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

def apply_mosaic(image, x, y, width, height, mosaic_size):
    # モザイク処理を適用する範囲を取得
    roi = image[y:y + height, x:x + width]
    # モザイク処理
    roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (width, height), interpolation=cv2.INTER_NEAREST)
    # モザイク処理を適用した部分を元の画像に戻す
    image[y:y + height, x:x + width] = roi
    return image

st.title("顔認識アプリ")
st.write("jpg画像をアップロードしてください。")

# モザイクのサイズを選択するスライダー
mosaic_size = st.slider('モザイクのサイズを選択してください (小さいほど細かい)', 1, 30, 10)

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
        # 各顔に対してモザイクを適用するかどうかを選択するチェックボックス
        for i, face in enumerate(faces):
            x, y, width, height = face['box']
            if st.checkbox(f"顔 {i+1} (信頼度: {face['confidence']:.2f})", key=f"face_{i}"):
                image_np = apply_mosaic(image_np, x, y, width, height, mosaic_size)
            # 検出された顔に矩形を描画
            cv2.rectangle(image_np, (x, y), (x + width, y + height), (255, 0, 0), 2)
    
    # 結果の画像を表示
    st.image(image_np, caption="認識結果", use_column_width=True)
