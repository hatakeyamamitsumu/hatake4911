import cv2
import streamlit as st
from ultralytics import YOLOWorld

# YOLO-Worldモデルの読み込み
model = YOLOWorld('yolov8x-world.pt')  # ダウンロードしたモデルのパスに置き換える

# 動画ファイルのアップロード
uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mov'])

# 動画ファイルが選択された場合
if uploaded_file is not None:
    # ファイルをメモリに読み込む
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)

    # OpenCVで動画を読み込む
    cap = cv2.VideoCapture(file_bytes)

    # 動画のフレームを順次処理
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 物体検出の実行
        results = model.predict(source=frame, conf=0.5, iou=0.45)

        # 結果の描画
        annotated_frame = results[0].plot()

        # Streamlitで画像を表示
        st.image(annotated_frame, channels="BGR")

    # 後処理
    cap.release()

# 静止画のアップロード
uploaded_image = st.file_uploader("Choose an image file", type=['jpg', 'png'])
if uploaded_image is not None:
    file_bytes = np.frombuffer(uploaded_image.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    results = model.predict(source=img, conf=0.5, iou=0.45)
    annotated_image = results[0].plot()
    st.image(annotated_image, channels="BGR")
