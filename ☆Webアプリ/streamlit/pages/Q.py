import streamlit as st
import cv2
import numpy as np

def main():
    st.title("画像重ね合わせアプリ")

    # 画像のアップロード
    uploaded_image1 = st.file_uploader("画像1をアップロードしてください", type=["jpg", "jpeg", "png"])
    uploaded_image2 = st.file_uploader("画像2をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image1 is not None and uploaded_image2 is not None:
        # 画像を読み込む
        image1 = cv2.imdecode(np.frombuffer(uploaded_image1.read(), np.uint8), 1)
        image2 = cv2.imdecode(np.frombuffer(uploaded_image2.read(), np.uint8), 1)

        # 画像のサイズを合わせる
        image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

        # 2枚目の画像を1/3に縮小
        height, width = image2.shape[:2]
        image2_resized = cv2.resize(image2, (int(width / 3), int(height / 3)))

        # 画像を重ねる
        overlay_image = cv2.addWeighted(image1, 0.5, image2_resized, 0.5, 0)

        # 重ねた画像を表示
        st.image(overlay_image, channels="BGR", caption="重ねた画像")

if __name__ == "__main__":
    main()
