import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
from io import BytesIO

st.set_page_config(layout="wide", page_title="Image Background Editor")

st.write("## 写真の背景を編集")
st.write("写真の背景を編集するアプリです。背景をぼかすか、完全に切り取るかを選択してください")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Function to blur the background and blend with the original image
def blur_and_blend(original, cutout, blur_radius):
    # Blur the original image
    original_blurred = original.filter(ImageFilter.GaussianBlur(blur_radius))
    # Composite the cutout onto the blurred original image
    original_blurred.paste(cutout, (0, 0), cutout)
    return original_blurred

# Function to remove the background completely
def remove_background(upload):
    image = Image.open(upload)
    cutout = remove(image)
    return cutout

# Main function for image processing based on user choice
def process_image(upload, blur_background, blur_radius):
    original_image = Image.open(upload)
    col1, col2 = st.columns(2)
    with col1:
        st.write("Original Image")
        st.image(original_image, use_column_width=True)

    with col2:
        if blur_background:
            st.write("Blurred Background Image")
            cutout = remove_background(upload)
            blurred_image = blur_and_blend(original_image, cutout, blur_radius)
            st.image(blurred_image, use_column_width=True)
        else:
            st.write("Cutout Image (Background Removed)")
            cutout = remove_background(upload)
            st.image(cutout, use_column_width=True)

    # Download button
    buf = BytesIO()
    if blur_background:
        blurred_image.save(buf, format='PNG')
        byte_im = buf.getvalue()
        st.sidebar.download_button("Download Blurred Background Image", byte_im, "blurred_background.png", "image/png")
    else:
        cutout.save(buf, format='PNG')
        byte_im = buf.getvalue()
        st.sidebar.download_button("Download Cutout Image", byte_im, "cutout_image.png", "image/png")

# Sidebar options
option = st.sidebar.radio("Choose Background Editing Option:", ("背景をぼかす", "背景を切り取る"))

if option == "Blur Background":
    blur_radius = st.sidebar.slider("Blur Radius", 0, 20, 5)
    uploaded_file = st.sidebar.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        if uploaded_file.size <= MAX_FILE_SIZE:
            process_image(upload=uploaded_file, blur_background=True, blur_radius=blur_radius)
        else:
            st.sidebar.error("Uploaded file is too large. Please upload an image smaller than 5MB.")
else:
    uploaded_file = st.sidebar.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        if uploaded_file.size <= MAX_FILE_SIZE:
            process_image(upload=uploaded_file, blur_background=False, blur_radius=0)
        else:
            st.sidebar.error("Uploaded file is too large. Please upload an image smaller than 5MB.")
