import streamlit as st
import numpy as np
from PIL import Image
import io

# Function to round each RGB value to the nearest multiple of 4
def round_to_nearest_multiple_of_4(value):
    return int(4 * round(value / 4))

# Function to convert image to nearest multiple of 4
def convert_to_nearest_multiple_of_4(image):
    # Convert image to numpy array
    image_array = np.array(image)

    # Apply rounding to each pixel's RGB value
    rounded_image_array = np.vectorize(round_to_nearest_multiple_of_4)(image_array)

    # Create PIL image from rounded array
    rounded_image = Image.fromarray(rounded_image_array.astype('uint8'))

    return rounded_image

# Streamlit app
st.title("写真のRGB値を最も近い4の倍数に変換")

# File uploader
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image
    image = Image.open(uploaded_file)

    # Convert image to nearest multiple of 4
    rounded_image = convert_to_nearest_multiple_of_4(image)

    # Display original and rounded images
    st.image([image, rounded_image], caption=["Original Image", "Rounded Image"], width=300)

    # Download button
    def download_image(image):
        # Convert PIL image to bytes
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()
        return img_byte_array

    if st.button("画像をダウンロード"):
        rounded_image_bytes = download_image(rounded_image)
        st.download_button(
            label="画像をダウンロード",
            data=rounded_image_bytes,
            file_name="rounded_image.png",
            mime="image/png"
        )
