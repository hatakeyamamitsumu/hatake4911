import streamlit as st
import numpy as np
from PIL import Image
import cv2

# Haar Cascadesの分類器を読み込む
car_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_car.xml')
# ファイルパスを直接指定する例
car_cascade = cv2.CascadeClassifier('/path/to/haarcascade_car.xml')

def detect_cars_haar(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in cars:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

# Streamlitアプリケーションの設定
st.title("車の検出アプリ")
st.write("画像をアップロードしてください。")

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file)
    image_np = np.array(image)  # OpenCV形式に変換

    # 車の検出を行う関数
    def detect_cars(image):
        result_image = np.copy(image)
        result_image = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)  # RGBをBGRに変換
        result_image = detect_cars_haar(result_image)
        result_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)  # BGRをRGBに変換
        return result_image

    # 検出実行
    result_image = detect_cars(image_np)

    # 結果の画像を表示
    st.image(result_image, caption="車の検出結果", use_column_width=True)
