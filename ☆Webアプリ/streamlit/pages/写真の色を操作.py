import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import cv2

# Function to adjust image
def adjust_image(image, r_value, g_value, b_value, contrast, brightness, sharpness, gamma, blur, hue, apply_canny=False):
    # RGB value adjustment
    image_array = np.array(image)
    modified_image_array_rgb = np.stack([image_array[:, :, 0] * (r_value / 255),
                                         image_array[:, :, 1] * (g_value / 255),
                                         image_array[:, :, 2] * (b_value / 255)], axis=-1)
    modified_image_rgb = Image.fromarray((modified_image_array_rgb).astype(np.uint8))

    # Contrast adjustment
    enhancer = ImageEnhance.Contrast(modified_image_rgb)
    modified_image_rgb = enhancer.enhance(contrast)

    # Brightness adjustment
    enhancer = ImageEnhance.Brightness(modified_image_rgb)
    modified_image_rgb = enhancer.enhance(brightness)

    # Sharpness adjustment
    modified_image_rgb = modified_image_rgb.filter(ImageFilter.UnsharpMask(radius=sharpness, percent=150))

    # Gamma correction adjustment
    modified_image_rgb = modified_image_rgb.point(lambda i: i**gamma)

    # Blur adjustment
    modified_image_rgb = modified_image_rgb.filter(ImageFilter.GaussianBlur(radius=blur))

    # Hue adjustment
    modified_image_hsv = modified_image_rgb.convert("HSV")
    modified_image_hsv_array = np.array(modified_image_hsv)
    modified_image_hsv_array[:, :, 0] = (modified_image_hsv_array[:, :, 0] + hue) % 256
    modified_image_rgb = Image.fromarray(modified_image_hsv_array, "HSV").convert("RGB")

    # Apply Canny edge detection
    if apply_canny:
        modified_image_rgb = cv2.Canny(np.array(modified_image_rgb), 50, 150)

    return modified_image_rgb

# Function to quantize image to specified number of colors
def quantize_image(image, num_colors):
    return image.quantize(colors=num_colors)

# Streamlit app
st.title("画像調整 & 色数変更アプリ")
st.write("写真の色のバランスを調節、写真の色数を減らすアプリを左のウィンドウで選択してご利用ください")
# Sidebar selection for app mode
app_mode = st.sidebar.selectbox("App Mode", ["画像調整", "色数変更"])

if app_mode == "画像調整":
    st.subheader("画像調整アプリ")

    # File uploader
    uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image
        image = Image.open(uploaded_file)
        st.image(image, caption="アップロードされた画像", use_column_width=True)
        
        # RGB value sliders
        r_value = st.slider("R値", 0, 255, 128)
        g_value = st.slider("G値", 0, 255, 128)
        b_value = st.slider("B値", 0, 255, 128)

        # Adjustment sliders
        contrast = st.slider("コントラスト", 0.0, 2.0, 1.0)
        brightness = st.slider("明るさ", 0.0, 2.0, 1.0)
        sharpness = st.slider("シャープネス", 0.0, 10.0, 1.0)
        gamma = st.slider("ガンマ補正", 0.1, 2.0, 1.0)
        blur = st.slider("ぼかし", 0.0, 10.0, 0.0)
        hue = st.slider("色相", -180, 180, 0)
        apply_canny = st.checkbox("Cannyエッジ検出を適用する")

        # Image adjustment
        modified_image = adjust_image(image, r_value, g_value, b_value, contrast, brightness, sharpness, gamma, blur, hue,
                                    apply_canny=apply_canny)

        # Display adjusted image
        st.image(modified_image, caption="調整後の画像", use_column_width=True)

        # Download button for adjusted image
        if st.button("画像をダウンロードしますか？"):
            modified_image_bytes = io.BytesIO()

            if apply_canny:
                # Convert Canny Edge NumPy array to PIL Image
                modified_image_canny = Image.fromarray(modified_image)
                modified_image_canny.save(modified_image_bytes, format='JPEG')
            else:
                modified_image.save(modified_image_bytes, format='JPEG')

            st.download_button("ダウンロード", modified_image_bytes.getvalue(), file_name="modified_image.jpg", key="download")

elif app_mode == "色数変更":
    st.subheader("色数変更アプリ")

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

        # Download button for quantized image
        if st.button("画像をダウンロードしますか？"):
            img_byte_array = io.BytesIO()
            quantized_image.save(img_byte_array, format='PNG')
            img_byte_array = img_byte_array.getvalue()

            st.download_button(
                label="ダウンロードボタン",
                data=img_byte_array,
                file_name="quantized_image.png",
                mime="image/png"
            )
