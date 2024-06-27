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
    # 検出された顔に矩形を描画して、顔の位置を返す
    face_positions = []
    for face in faces:
        x, y, width, height = face['box']
        face_positions.append((x, y, width, height))
    return face_positions

def apply_mosaic(image, face_positions, scale=0.5):
    for (x, y, width, height) in face_positions:
        # 顔の部分を切り取る
        face = image[y:y+height, x:x+width]
        # 顔の部分にモザイク処理を適用
        face = cv2.resize(face, (0, 0), fx=scale, fy=scale)
        face = cv2.resize(face, (width, height), interpolation=cv2.INTER_NEAREST)
        # モザイクをかけた顔を元の画像に戻す
        image[y:y+height, x:x+width] = face
    return image

st.title("顔認識とモザイク処理アプリ")
st.write("jpg画像をアップロードしてください")

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file)
    # OpenCV形式に変換
    image_cv = np.array(image)
    # 顔認識を実行し、顔の位置を取得
    face_positions = detect_faces(image_cv.copy())

    # 検出された顔をチェックボックスで選択
    selected_faces = []
    for i, (x, y, width, height) in enumerate(face_positions):
        if st.checkbox(f"顔 {i+1} (x={x}, y={y}, w={width}, h={height})"):
            selected_faces.append((x, y, width, height))

    if selected_faces:
        # 選択された顔にモザイク処理を適用
        result_image_mosaic = apply_mosaic(image_cv, selected_faces)
        # モザイクをかけた結果の画像を表示
        st.image(result_image_mosaic, caption="モザイク処理後の画像", use_column_width=True)
    else:
        # 選択されなかった場合は元の画像を表示
        st.image(image_cv, caption="元の画像", use_column_width=True)
