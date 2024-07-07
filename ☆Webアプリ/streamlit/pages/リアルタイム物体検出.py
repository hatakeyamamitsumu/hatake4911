import streamlit as st
import cv2
from PIL import Image
import numpy as np

def main():
    # Streamlitアプリケーションの設定
    st.title("PCカメラの映像を表示するアプリ")

    # OpenCVを使用してPCカメラからの映像を取得する
    cap = cv2.VideoCapture(0)  # 0はデフォルトのカメラを指定することを意味します

    if not cap.isOpened():
        st.error("カメラを開けませんでした。")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("カメラからの映像を取得できませんでした。")
            break

        # OpenCVのBGR形式からRGB形式に変換
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # フレームをPIL Imageに変換
        pil_image = Image.fromarray(frame_rgb)

        # Streamlitで画像を表示
        st.image(pil_image, channels="RGB")

        # "Q"を押すとアプリを終了する
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 後片付け
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
