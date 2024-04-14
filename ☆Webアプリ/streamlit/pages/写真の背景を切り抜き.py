import streamlit as st
import numpy as np
from PIL import Image, ImageFilter
import io
import cv2

st.set_page_config(layout="wide", page_title="Image Background Editor")

st.write("## 写真の背景を編集")
st.write("写真の背景を編集するアプリです。背景をぼかすか、完全に切り取るかを選択してください。")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Function to remove background using OpenCV
def remove_background(image_array):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

    # Apply Gaussian Blur to smooth the image
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Use adaptive thresholding to segment the foreground (person) from the background
    _, mask = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)

    # Invert the mask
    mask = cv2.bitwise_not(mask)

    # Apply the mask to the original image to remove the background
    result = cv2.bitwise_and(image_array, image_array, mask=mask)

    return result

# Function to blur the background and blend with the original image
def blur_and_blend(original, cutout, blur_radius):
    # Blur the original image
    original_blurred = original.filter(ImageFilter.GaussianBlur(blur_radius))
    # Composite the cutout onto the blurred original image
    original_blurred.paste(cutout, (0, 0), cutout)
    return original_blurred

# Main function for image processing based on user choice
def process_image(upload, background_option, blur_radius):
    image = Image.open(upload)
    col1, col2 = st.columns(2)
    with col1:
        st.write("Original Image")
        st.image(image, use_column_width=True)

    with col2:
        if background_option == "Blur Background":
            st.write("Blurred Background Image")
            blurred_image = image.filter(ImageFilter.GaussianBlur(blur_radius))
            st.image(blurred_image, use_column_width=True)
        elif background_option == "Remove Background":
            st.write("Background Removed Image")
            image_array = np.array(image)
            cutout = remove_background(image_array)
            st.image(cutout, use_column_width=True)

    # Download button
    buf = io.BytesIO()
    if background_option == "Blur Background":
        blurred_image.save(buf, format='PNG')
        byte_im = buf.getvalue()
        st.sidebar.download_button("Download Blurred Background Image", byte_im, "blurred_background.png", "image/png")
    elif background_option == "Remove Background":
        cutout = Image.fromarray(cutout)
        cutout.save(buf, format='PNG')
        byte_im = buf.getvalue()
        st.sidebar.download_button("Download Cutout Image", byte_im, "cutout_image.png", "image/png")

# Sidebar options
background_option = st.sidebar.radio("Choose Background Editing Option:", ("Blur Background", "Remove Background"))
blur_radius = st.sidebar.slider("Blur Radius", 0, 20, 5)
uploaded_file = st.sidebar.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    if uploaded_file.size <= MAX_FILE_SIZE:
        process_image(upload=uploaded_file, background_option=background_option, blur_radius=blur_radius)
    else:
        st.sidebar.error("Uploaded file is too large. Please upload an image smaller than 5MB.")
