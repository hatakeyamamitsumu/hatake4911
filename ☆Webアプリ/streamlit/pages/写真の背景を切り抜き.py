import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Remove background from your image")
st.write(
    ":dog: Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available [here](https://github.com/tyler-simons/BackgroundRemoval) on GitHub. Special thanks to the [rembg library](https://github.com/danielgatis/rembg) :grin:"
)
st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Function to remove background from the image
def remove_background(image):
    with st.spinner("Removing background..."):
        image_array = Image.open(image)
        return remove(image_array)

# Download the image
def download_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def fix_image(upload, process_option):
    if process_option == "Remove Background":
        fixed_image = remove_background(upload)
    else:
        fixed_image = upload

    col1.write("Original Image :camera:")
    col1.image(upload)

    col2.write("Fixed Image :wrench:")
    col2.image(fixed_image)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download fixed image", download_image(fixed_image), "fixed.png", "image/png")

col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
process_option = st.sidebar.radio("Choose processing option:", ("Original Image", "Remove Background"))

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        fix_image(upload=my_upload, process_option=process_option)
