import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(layout="wide", page_title="写真の背景を削除")

st.write("写真の背景を切り取ります。左のウインドウから写真をアップロードしてください。")

st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Download the fixed image
def convert_image(img):
    return img


def fix_image(upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    # 背景を削除してバイト列を取得
    byte_im = remove(image)

    # バイト列から画像を作成
    fixed = Image.open(BytesIO(byte_im))

    col2.write("Fixed Image :wrench:")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    
    # ダウンロードボタン
    st.sidebar.download_button("ダウンロード", convert_image(fixed), "fixed.png", "image/png")


col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("写真をアップロードしてください。", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("ファイルサイズが大きすぎます。5MB以内でお願いします。")
    else:
        fix_image(upload=my_upload)
