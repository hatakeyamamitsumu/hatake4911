import cv2
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from ultralytics import YOLO
import os

# モデルのパスを環境変数から取得（例）
MODEL_PATH = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s-pose.pt'
def load_model(model_path):
    model = YOLO(model_path)
    return model

# 画像処理
def process_image(img, model):
    # 画像処理のロジック
    results = model(img)
    
    # 一時ファイルのパスを生成
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成
    temp_file = os.path.join(temp_dir, "result.jpg")
    
    # 画像を保存
    cv2.imwrite(temp_file, results[0].plot())
    
    return temp_file

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
            results = process_image(img_rgb, model)

            # ダウンロードボタンの追加
            with open(results, "rb") as f:
                st.download_button(
                    label="ダウンロード",
                    data=f.read(),
                    file_name="result.jpg",
                    mime='image/jpeg'
                )

            # 一時ファイルを削除
            os.remove(results)
        elif uploaded_file.type == "video/mp4":
            # 動画処理
            process_video(uploaded_file, model)

if __name__ == "__main__":
    main()
