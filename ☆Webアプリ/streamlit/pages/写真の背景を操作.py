import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
from io import BytesIO
import base64

st.set_page_config(layout="wide", page_title="Image Editor")

st.write("## 背景編集ツール")
st.text("参考資料：https://bgremoval.streamlit.app/")
st.write("左のウィンドウから画像をアップロードしてください")

st.sidebar.write("## 操作設定 :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Download the image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def remove_background(image):
    col1.write("Original Image :camera:")
    col1.image(image)

    fixed = remove(image)
    col2.write("Background Removed Image :wrench:")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("ダウンロード", convert_image(fixed), "background_removed.png", "image/png")

def blur_background(image, blur_radius):
    col1.write("Original Image :camera:")
    col1.image(image)

    original_blurred = image.filter(ImageFilter.GaussianBlur(blur_radius))

    # Background removal
    cutout = remove(image)

    # Blending blurred background with cutout
    blended_image = fix_and_blend_images(original_blurred, cutout, blur_radius)

    col2.write("Blurred Image :wrench:")
    col2.image(blended_image)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("ダウンロード", convert_image(blended_image), "blurred_image.png", "image/png")

def fix_and_blend_images(original, cutout, blur_radius):
    original.paste(cutout, (0, 0), cutout)
    return original

col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("ファイルサイズが大きすぎます。5MB以内でお願いします。")
    else:
        operation = st.sidebar.radio("操作を選択してください", ("背景を削除", "背景をぼかす"))
        if operation == "背景を削除":
            remove_background(Image.open(my_upload))
        elif operation == "背景をぼかす":
            blur_radius = st.sidebar.slider("ぼかし具合", 0, 20, 5)
            blur_background(Image.open(my_upload), blur_radius)
else:
    st.write("アップロードされた画像がありません。")
