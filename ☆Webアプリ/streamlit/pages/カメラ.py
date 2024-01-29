import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def apply_binary_threshold(image, threshold_value):
    _, binary_img = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return binary_img

def apply_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_blur(image, kernel_size):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def apply_canny_edge(image, low_threshold, high_threshold):
    return cv2.Canny(image, low_threshold, high_threshold)

def main():
    st.title("Real-time Image Processing")

    # Image input options
    picture = st.camera_input("Take a picture")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        picture = Image.open(uploaded_image)

    processed_img = None

    if picture is not None:
        img = np.array(picture)

        st.image(picture, caption='Input Image', use_column_width=True)

        # Camera settings
        brightness = st.slider("Brightness", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        contrast = st.slider("Contrast", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        saturation = st.slider("Saturation", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

        # Apply camera settings
        img = cv2.convertScaleAbs(img, alpha=brightness, beta=0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img[..., 1] = img[..., 1] * contrast
        img[..., 2] = img[..., 2] * saturation
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

        # Filter options
        filter_options = st.multiselect("Select Filters", ["Binary Threshold", "Grayscale", "Blur", "Canny Edge"])

        for filter_option in filter_options:
            if filter_option == "Binary Threshold":
                threshold_value = st.slider("Threshold Value", min_value=0, max_value=255, value=127, step=1)
                img = apply_binary_threshold(img, threshold_value)
            elif filter_option == "Grayscale":
                img = apply_grayscale(img)
            elif filter_option == "Blur":
                kernel_size = st.slider("Kernel Size", min_value=1, max_value=31, value=5, step=2)
                img = apply_blur(img, kernel_size)
            elif filter_option == "Canny Edge":
                low_threshold = st.slider("Low Threshold", min_value=0, max_value=255, value=50, step=1)
                high_threshold = st.slider("High Threshold", min_value=0, max_value=255, value=150, step=1)
                img = apply_canny_edge(img, low_threshold, high_threshold)

        st.image(img, caption='Processed Image', use_column_width=True)

        # Save processed image to BytesIO
        processed_img_io = BytesIO()
        pil_processed_img = Image.fromarray(img)
        pil_processed_img.save(processed_img_io, format='PNG')

        # Download button
        st.download_button(
            label="Download Processed Image",
            data=processed_img_io.getvalue(),
            file_name="processed_image.png",
            key="download_button",
        )

if __name__ == "__main__":
    main()
