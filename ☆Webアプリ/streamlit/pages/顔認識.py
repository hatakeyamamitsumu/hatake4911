import streamlit as st
import numpy as np
from PIL import Image
import dlib

# Dlibの顔検出器を読み込む
detector = dlib.get_frontal_face_detector()

def detect_faces(image):
    # グレースケールに変換
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 顔を検出
    faces = detector(gray_image)
    # 検出された顔に矩形を描画
    for face in faces:
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return image

st.title("顔認識アプリ")
st.write("画像をアップロードしてください。")

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
