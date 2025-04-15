import streamlit as st
import numpy as np
from PIL import Image
import cv2
import os

# Haarカスケードのディレクトリパスを指定
cascade_dir = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/haarcascade特徴分類器/'

# ディレクトリ内のHaarカスケードファイルをリストアップ
if os.path.exists(cascade_dir):
    cascade_files = [f for f in os.listdir(cascade_dir) if f.endswith('.xml')]
else:
    cascade_files = []

def load_cascade(file_name):
    return cv2.CascadeClassifier(os.path.join(cascade_dir, file_name))

def detect_objects(image, cascade, scaleFactor=1.1, minNeighbors=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    objects = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=(30, 30))
    for (x, y, w, h) in objects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

# Streamlitアプリケーションの設定
st.title("物体検出アプリ")
st.write("画像をアップロードし、使用するHaarカスケードを選択してください。")

if not cascade_files:
    st.error("Haarカスケードファイルが見つかりません。ディレクトリパスを確認してください。")

# Haarカスケードファイルの選択
cascade_file = st.selectbox("Haarカスケードファイルを選択", cascade_files) if cascade_files else None

# 画像のアップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and cascade_file is not None:
    try:
        # アップロードされた画像を読み込む
        image = Image.open(uploaded_file)
        image_np = np.array(image)  # OpenCV形式に変換

        # 選択されたHaarカスケードファイルを読み込む
        cascade = load_cascade(cascade_file)

        # 物体の検出を行う関数
        def detect_and_display(image, cascade, scaleFactor=1.1, minNeighbors=5):
            result_image = np.copy(image)
            result_image = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)  # RGBをBGRに変換
            result_image = detect_objects(result_image, cascade, scaleFactor, minNeighbors)
            result_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)  # BGRをRGBに変換
            return result_image

        # パラメータの設定
        scaleFactor = st.slider("scaleFactor(1.1から1.4の範囲で調整するのが一般的です)", 1.01, 1.5, 1.1)
        minNeighbors = st.slider("minNeighbors(誤検出が多い場合は値を大きく、検出率が低い場合は値を小さくしてください。)", 1, 10, 5)

        # 検出実行
        result_image = detect_and_display(image_np, cascade, scaleFactor, minNeighbors)

        # 結果の画像を表示
        st.image(result_image, caption="物体検出結果", use_column_width=True)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    if uploaded_file is None:
        st.warning("画像をアップロードしてください。")
    if cascade_file is None:
        st.warning("Haarカスケードファイルを選択してください。")
