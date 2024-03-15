import streamlit as st
from PIL import Image
import io

# Function to quantize image to specified number of colors
def quantize_image(image, num_colors):
    return image.quantize(colors=num_colors)

# Streamlit app
st.title("色数を変えて画像を保存")
st.write('写真の色数を減らします。')
# File uploader
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

# Color slider
num_colors = st.slider("色数", min_value=2, max_value=256, value=256, step=1)

if uploaded_file is not None:
    # Read the image
    image = Image.open(uploaded_file)

    # Convert image to specified number of colors
    quantized_image = quantize_image(image, num_colors)

    # Display quantized image
    st.image(quantized_image, caption=f"{num_colors}色に変換された画像", use_column_width=True)

    # Download button
    def download_image(image):
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()
        return img_byte_array

    if st.button("画像をダウンロード"):
        rounded_image_bytes = download_image(quantized_image)
        st.download_button(
            label="画像をダウンロード",
            data=rounded_image_bytes,
            file_name="quantized_image.png",
            mime="image/png"
        )
