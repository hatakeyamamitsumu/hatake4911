import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import cv2
from rembg import remove

def fix_and_blend_images(original_blurred, cutout, blur_radius):
    # Create a mask from the cutout image
    cutout_np = np.array(cutout)
    mask = cutout_np[:, :, 3] > 0  # Assuming cutout is an RGBA image
    mask = mask.astype(np.uint8) * 255

    # Convert images to OpenCV format
    original_blurred_cv = cv2.cvtColor(np.array(original_blurred), cv2.COLOR_RGB2BGR)
    cutout_cv = cv2.cvtColor(np.array(cutout)[:, :, :3], cv2.COLOR_RGB2BGR)

    # Blur the background where mask is not present
    blurred_background = cv2.GaussianBlur(original_blurred_cv, (2 * blur_radius + 1, 2 * blur_radius + 1), 0)

    # Combine the cutout with the blurred background
    blended = np.where(mask[:, :, None] == 255, cutout_cv, blurred_background)

    # Convert back to PIL format
    blended_image = Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
    return blended_image

def convert_image(img):
    # Convert the PIL image to bytes
    from io import BytesIO
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def main():
    st.title("画像の背景をぼかすアプリ")

    uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
    blur_radius = st.sidebar.slider("ぼかしの強さ (半径)", min_value=1, max_value=50, value=10)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)

        col1.write("オリジナル画像 :camera:")
        col1.image(image)

        original_blurred = image.filter(ImageFilter.GaussianBlur(blur_radius))

        # 背景の除去
        cutout = remove(image)

        # ぼかし背景と切り抜きをブレンド
        blended_image = fix_and_blend_images(original_blurred, cutout, blur_radius)

        col2.write("ぼかし画像 :wrench:")
        col2.image(blended_image)

        st.sidebar.markdown("\n")
        st.sidebar.download_button(
            "ダウンロード", convert_image(blended_image), "blurred_image.png", "image/png"
        )

if __name__ == "__main__":
    main()
