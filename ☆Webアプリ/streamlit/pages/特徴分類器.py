import streamlit as st
import numpy as np
from PIL import Image
import cv2

# Haarカスケードのファイルパスを指定
cascade = cv2.CascadeClassifier('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/haarcascade特徴分類器/haarcascade_fullbody.xml')

def detect_objects(image, scaleFactor=1.1, minNeighbors=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    objects = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=(30, 30))
    for (x, y, w, h) in objects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

# Streamlitアプリケーションの設定
st.title("物体検出アプリ")
st.write("画像をアップロードしてください。")

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file)
    image_np = np.array(image)  # OpenCV形式に変換

    # 物体の検出を行う関数
    def detect_and_display(image, scaleFactor=1.1, minNeighbors=5):
        result_image = np.copy(image)
        result_image = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)  # RGBをBGRに変換
        result_image = detect_objects(result_image, scaleFactor, minNeighbors)
        result_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)  # BGRをRGBに変換
        return result_image

    # パラメータの設定
    scaleFactor = st.slider("scaleFactor", 1.01, 1.5, 1.1)
    minNeighbors = st.slider("minNeighbors", 1, 10, 5)

    # 検出実行
    result_image = detect_and_display(image_np, scaleFactor, minNeighbors)

    # 結果の画像を表示
    st.image(result_image, caption="物体検出結果", use_column_width=True)
