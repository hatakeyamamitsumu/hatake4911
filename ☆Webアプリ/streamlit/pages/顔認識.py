import cv2
import streamlit as st
import numpy as np
from PIL import Image

顔認識用のHaarカスケードファイルのパスを指定
face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

Haarカスケード分類器を読み込む
face_cascade = cv2.CascadeClassifier(face_cascade_path)

def detect_faces(image):
# グレースケールに変換
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

gray_image = cv2.equalizeHist(gray_image)
# 顔を検出
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=3, minSize=(30, 30))

# 検出された顔に矩形を描画
for (x, y, w, h) in faces:
cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
return image

st.title("顔認識アプリ")
st.write("画像をアップロードしてください。")

画像のアップロード
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
