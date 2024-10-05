import streamlit as st
import cv2

# カメラから画像を取得
picture = st.camera_input("Take a picture")

if picture:
    # OpenCVで画像を読み込む
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
