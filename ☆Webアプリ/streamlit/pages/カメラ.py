import streamlit as st
import cv2
import numpy as np

def apply_binary_threshold(image, threshold_value):
    # 二値化の処理
    _, binary_img = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return binary_img

def main():
    st.title("Real-time Image Processing")

    # カメラ入力
    picture = st.camera_input("Take a picture")

    # 画像を表示
    st.image(picture, caption='Captured Image', use_column_width=True)

    # ボタンで二値化を適用
    threshold_value = st.slider("Threshold Value", min_value=0, max_value=255, value=127, step=1)
    if st.button("Apply Binary Threshold"):
        # カメラ画像をNumPy配列に変換
        img = cv2.imdecode(np.frombuffer(picture, np.uint8), 1)

        # 二値化処理
        binary_img = apply_binary_threshold(img, threshold_value)

        # 二値化後の画像を表示
        st.image(binary_img, caption=f'Binary Threshold (Threshold Value: {threshold_value})', use_column_width=True)

if __name__ == "__main__":
    main()

