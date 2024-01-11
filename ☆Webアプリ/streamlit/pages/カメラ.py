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

            # フィルタと処理オプション
            filter_option = st.selectbox("Select Filter", ["Binary Threshold", "Grayscale", "Blur", "Canny Edge"])
            if filter_option == "Binary Threshold":
                # ボタンで二値化を適用
                threshold_value = st.slider("Threshold Value", min_value=0, max_value=255, value=127, step=1)
                if st.button("Apply Binary Threshold"):
                    processed_img = apply_binary_threshold(img, threshold_value)
            elif filter_option == "Grayscale":
                processed_img = apply_grayscale(img)
            elif filter_option == "Blur":
                # ボタンでぼかしを適用
                kernel_size = st.slider("Kernel Size", min_value=1, max_value=31, value=5, step=2)
                if st.button("Apply Blur"):
                    processed_img = apply_blur(img, kernel_size)
            elif filter_option == "Canny Edge":
                # ボタンでCannyエッジ検出を適用
                low_threshold = st.slider("Low Threshold", min_value=0, max_value=255, value=50, step=1)
                high_threshold = st.slider("High Threshold", min_value=0, max_value=255, value=150, step=1)
                if st.button("Apply Canny Edge"):
                    processed_img = apply_canny_edge(img, low_threshold, high_threshold)

            if filter_option != "Binary Threshold":
                # PIL形式に変換して表示
                pil_processed_img = Image.fromarray(processed_img)
                st.image(pil_processed_img, caption=f'{filter_option} Filter', use_column_width=True)

                # Save processed image to BytesIO
                processed_img_io = BytesIO()
                pil_processed_img.save(processed_img_io, format='PNG')

                # Download button
                st.download_button(
                    label=f"Download {filter_option} Image",
                    data=processed_img_io.getvalue(),
                    file_name=f"{filter_option.lower().replace(' ', '_')}_image.png",
                    key="download_button",
                )

if __name__ == "__main__":
    main()

