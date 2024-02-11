import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
from io import BytesIO
import base64

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## 写真の背景をぼかす")
st.write("背景を切り抜きたい写真を、左のウインドウからアップロードしてください＜＜")
st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def fix_and_blend_images(original, cutout, blur_radius):
    # 元の画像をぼかす
    original_blurred = original.filter(ImageFilter.GaussianBlur(blur_radius))

    # 切り抜いた画像をもとの画像の上に合成
    original_blurred.paste(cutout, (0, 0), cutout)

    return original_blurred

def fix_image(upload, blur_radius):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    # ぼかし効果を適用した元の画像を作成
    original_blurred = image.filter(ImageFilter.GaussianBlur(blur_radius))

    # 切り抜き処理
    cutout = remove(image)

    # 合成してぼかし効果を適用
    blended_image = fix_and_blend_images(original_blurred, cutout, blur_radius)

    col2.write("Fixed and Blurred Image :wrench:")
    col2.image(blended_image)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("ダウンロードボタン", convert_image(blended_image), "blended_image.png", "image/png")

col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("ここからアップロードしてください", type=["png", "jpg", "jpeg"])
blur_radius = st.sidebar.slider("ぼかし具合", 0, 20, 5)  # You can adjust the min, max, and default values as needed.

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        fix_image(upload=my_upload, blur_radius=blur_radius)
else:
    fix_image("/mount/src/hatake4911/☆Webアプリ/画像/skytree.png", blur_radius=blur_radius)
