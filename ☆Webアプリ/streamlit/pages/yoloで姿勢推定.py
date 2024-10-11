
import matplotlib.pyplot as plt
import numpy as np



import cv2
from ultralytics import YOLO
import streamlit as st

# モデルのパスを環境変数から取得（例）
MODEL_PATH = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s-pose.pt'  # Replace with your actual path
# モデルのロード
def load_model(model_path):
    model = YOLO(model_path)
    return model

# 画像処理
def process_image(img, model):
    # 画像処理のロジック
    results = model(img)
    # ... (画像処理の結果を表示するなど)
    return results

# 動画処理
def process_video(video_path, model):
    # 動画処理のロジック
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # フレームを処理
        results = process_image(frame, model)

        # 結果を表示
        cv2.imshow('Video', results[0].plot())
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# メイン関数
def main():
    # StreamlitのUI設定
    st.title("YOLOv8 姿勢推定")
    uploaded_file = st.file_uploader("画像または動画を選択してください", type=["png", "jpg", "jpeg", "mp4"])

    # モデルのロード
    model = load_model(MODEL_PATH)

    # アップロードされたファイルの処理
    if uploaded_file is not None:
        # ファイルの種類によって処理を分岐
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            # 画像処理　
            bytes_data = uploaded_file.read()
            np_array = np.frombuffer(bytes_data, np.uint8)
            img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = process_image(imgimg_rgb, model)
            
            st.image(results[0].plot())
        elif uploaded_file.type == "video/mp4":
            # 動画処理
            process_video(uploaded_file, model)

if __name__ == "__main__":
    main()
