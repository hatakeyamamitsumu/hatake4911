import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np

#  モデルの読み込み (パスを適宜変更)
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolo11s.pt')
# YOLOv8モデルのロード
#model = YOLOWorld('yolov8s.pt')  # モデルのパスを適宜変更

# カメラ入力
picture = st.camera_input("写真を撮ってください")

if picture:
    # OpenCVで画像を読み込む
    byte_arr = np.frombuffer(picture.read(), np.uint8)
    cv_image = cv2.imdecode(byte_arr, cv2.IMREAD_COLOR)

    # YOLOv8で物体検出
    results = model.predict(source=cv_image)

    # 結果を可視化
    annotated_frame = results[0].plot()

    # 画像を表示
    st.image(annotated_frame, channels="BGR")

    # 画像を保存し、ダウンロードボタンを表示
    cv2.imwrite("detected_image.jpg", annotated_frame)
    with open("detected_image.jpg", "rb") as file:
        st.download_button(
            label="検出結果をダウンロード",
            data=file,
            file_name="detected_image.jpg",
            mime="image/jpeg"
        )
