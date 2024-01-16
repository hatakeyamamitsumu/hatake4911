import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import cv2

def adjust_image(image, r_value, g_value, b_value, contrast, brightness, sharpness, gamma, blur, hue, apply_canny=False):
    # RGB値の調整
    image_array = np.array(image)
    modified_image_array_rgb = np.stack([image_array[:, :, 0] * (r_value / 255),
                                         image_array[:, :, 1] * (g_value / 255),
                                         image_array[:, :, 2] * (b_value / 255)], axis=-1)
    modified_image_rgb = Image.fromarray((modified_image_array_rgb).astype(np.uint8))

    # コントラストの調整
    enhancer = ImageEnhance.Contrast(modified_image_rgb)
    modified_image_rgb = enhancer.enhance(contrast)

    # 明るさの調整
    enhancer = ImageEnhance.Brightness(modified_image_rgb)
    modified_image_rgb = enhancer.enhance(brightness)

    # シャープネスの調整
    modified_image_rgb = modified_image_rgb.filter(ImageFilter.UnsharpMask(radius=sharpness, percent=150))

    # ガンマ補正の調整
    modified_image_rgb = modified_image_rgb.point(lambda i: i**gamma)

    # ぼかしの調整
    modified_image_rgb = modified_image_rgb.filter(ImageFilter.GaussianBlur(radius=blur))

    # 色相の調整
    modified_image_hsv = modified_image_rgb.convert("HSV")
    modified_image_hsv_array = np.array(modified_image_hsv)
    modified_image_hsv_array[:, :, 0] = (modified_image_hsv_array[:, :, 0] + hue) % 256
    modified_image_rgb = Image.fromarray(modified_image_hsv_array, "HSV").convert("RGB")

    # Cannyエッジ検出の適用
    if apply_canny:
        modified_image_rgb = cv2.Canny(np.array(modified_image_rgb), 50, 150)

    return modified_image_rgb

# Streamlit アプリのタイトル
st.title("画像調整アプリ")
st.write("調整後の画像は画面の一番下に表示されます")
# 画像のアップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # アップロードされた画像を表示
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_column_width=True)
    
    # RGB値のスライダーを作成
    r_value = st.slider("R値", 0, 255, 128)
    g_value = st.slider("G値", 0, 255, 128)
    b_value = st.slider("B値", 0, 255, 128)

    # コントラスト、明るさ、シャープネス、ガンマ補正、ぼかし、色相、Cannyエッジ検出のスライダーを作成
    contrast = st.slider("コントラスト", 0.0, 2.0, 1.0)
    brightness = st.slider("明るさ", 0.0, 2.0, 1.0)
    sharpness = st.slider("シャープネス", 0.0, 10.0, 1.0)
    gamma = st.slider("ガンマ補正", 0.1, 2.0, 1.0)
    blur = st.slider("ぼかし", 0.0, 10.0, 0.0)
    hue = st.slider("色相", -180, 180, 0)
    apply_canny = st.checkbox("Cannyエッジ検出を適用する")

    # 画像の調整
    modified_image = adjust_image(image, r_value, g_value, b_value, contrast, brightness, sharpness, gamma, blur, hue,
                                  apply_canny=apply_canny)

    # 調整された画像を表示
    st.image(modified_image, caption="調整後の画像", use_column_width=True)

    # 調整された画像をダウンロード
    if st.button("画像をダウンロードしますか？"):
        # Pillowで画像を作成し、バイトデータに変換
        modified_image_bytes = io.BytesIO()

        if apply_canny:
            # Convert Canny Edge NumPy array to PIL Image
            modified_image_canny = Image.fromarray(modified_image_rgb)
            modified_image_canny.save(modified_image_bytes, format='JPEG')
        else:
            modified_image.save(modified_image_bytes, format='JPEG')

        # ダウンロードボタンに渡す
        st.download_button("ダウンロード", modified_image

