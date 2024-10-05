import streamlit as st
import cv2

# Camera input with correct indentation
picture = st.camera_input("Take a picture")

if picture:
    # OpenCV image processing
    byte_arr = np.frombuffer(picture.read(), np.uint8)
    cv_image = cv2.imdecode(byte_arr, cv2.IMREAD_COLOR)

    # 画像を保存する
    cv2.imwrite("captured_image.jpg", cv_image)

    # ダウンロードボタンを表示
    with open("captured_image.jpg", "rb") as file:
        st.download_button(
            label="Download image",
            data=file,
            file_name="captured_image.jpg",
            mime="image/jpeg"
        )
