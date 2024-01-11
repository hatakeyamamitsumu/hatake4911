import streamlit as st
import cv2
import numpy as np
from PIL import Image

def apply_binary_threshold(image, threshold_value):
    # 二値化の処理
    _, binary_img = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return binary_img

def main():
    st.title("Real-time Image Processing")

    # カメラ入力
    picture = st.camera_input("Take a picture")

    if picture is not None:
        # Convert camera input to NumPy array
        img = np.frombuffer(picture.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(img, 1)

        if img is not None:
            # PIL形式に変換
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            # 画像を表示
            st.image(pil_img, caption='Captured Image', use_column_width=True)

            # ボタンで二値化を適用
            threshold_value = st.slider("Threshold Value", min_value=0, max_value=255, value=127, step=1)
            if st.button("Apply Binary Threshold"):
                # 二値化処理
                binary_img = apply_binary_threshold(img, threshold_value)

                # PIL形式に変換して表示
                pil_binary_img = Image.fromarray(binary_img)
                st.image(pil_binary_img, caption=f'Binary Threshold (Threshold Value: {threshold_value})', use_column_width=True)

if __name__ == "__main__":
    main()

