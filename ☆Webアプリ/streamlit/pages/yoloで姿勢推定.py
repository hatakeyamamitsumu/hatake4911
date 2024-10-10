import streamlit as st
from ultralytics import YOLO

# モデルのロード
model = YOLO("yolov8n-pose.pt")  # 姿勢推定モデル

# タイトル設定
st.title("YOLOによる姿勢推定アプリ")

# 画像アップロード
uploaded_file = st.file_uploader("画像を選択してください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 画像の読み込み
    img = uploaded_file.read()
    # 推論実行
    results = model(img)
    # 結果の表示
    for img in results.imgs:
        st.image(img)
