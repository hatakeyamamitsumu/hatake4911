import streamlit as st
from PIL import Image, ImageFilter
from io import BytesIO

st.set_page_config(layout="wide", page_title="Image Background Editor")

st.write("## Edit Your Image Background")
st.write(
    "Upload an image and choose whether to remove the background or blur it. Full quality images can be downloaded from the sidebar."
)
st.sidebar.write("## Upload and download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Function to remove background from the image
def remove_background(image):
    with st.spinner("Removing background..."):
        image_array = Image.open(image)
        return remove(image_array)

# Function to blur the background
def blur_background(image, blur_radius):
    with st.spinner("Blurring background..."):
        return image.filter(ImageFilter.GaussianBlur(blur_radius))

# Download the image
def download_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def fix_image(upload, process_option, blur_radius):
    if process_option == "Remove Background":
        fixed_image = remove_background(upload)
    elif process_option == "Blur Background":
        fixed_image = blur_background(upload, blur_radius)
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
process_option = st.sidebar.radio("Choose processing option:", ("Original Image", "Remove Background", "Blur Background"))
blur_radius = st.sidebar.slider("Blur Radius", 0, 20, 5)

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        fix_image(upload=my_upload, process_option=process_option, blur_radius=blur_radius)
