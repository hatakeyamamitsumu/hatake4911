import streamlit as st
from ultralytics import YOLO

# モデルのロード  https://github.com/hatakeyamamitsumu/hatake4911/blob/main/%E2%98%86Web%E3%82%A2%E3%83%97%E3%83%AA/%E3%81%9D%E3%81%AE%E4%BB%96%E9%87%8D%E8%A6%81%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB/yolo11s-pose.pt
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
