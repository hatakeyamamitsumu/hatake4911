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
    # 顔の位置を取得
    face_positions = [(face['box'][0], face['box'][1], face['box'][2], face['box'][3]) for face in faces]
    return face_positions

def apply_mosaic(image, face_positions, scale=0.1):
    for (x, y, width, height) in face_positions:
        # 顔の部分を切り取る
        face = image[y:y+height, x:x+width]
        # 顔の部分にモザイク処理を適用
        face = cv2.resize(face, (0, 0), fx=scale, fy=scale)
        face = cv2.resize(face, (width, height), interpolation=cv2.INTER_NEAREST)
        # モザイクをかけた顔を元の画像に戻す
        image[y:y+height, x:x+width] = face
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
    face_positions = detect_faces(image)
    # モザイク処理を適用
    result_image = apply_mosaic(image, face_positions)
    # 結果の画像を表示
    st.image(result_image, caption="認識結果", use_column_width=True)
