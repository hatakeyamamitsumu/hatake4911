import io
import streamlit as st
from PIL import Image
import pytesseract

# 画像をアップロード
uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # アップロードされた画像をPillowのImageオブジェクトに変換
    image = Image.open(uploaded_image)

    # 画像からテキストをOCRで取得
    text = pytesseract.image_to_string(image)

    # OCRで取得したテキストを出力
    st.text("OCRで取得したテキスト:")
    st.text(text)
