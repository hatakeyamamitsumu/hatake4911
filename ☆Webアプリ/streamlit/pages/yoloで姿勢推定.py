import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO

# モデルのパス
MODEL_PATH = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolo11s-pose.pt'  # 自分のモデルのパスに置き換えてください

def load_model(model_path):
    model = YOLO(model_path)
    return model

def process_image(img, model):
    # 画像処理のロジック
    results = model(img)

    # 結果を画像に描画
    result_img = results[0].plot()

    # 画像を保存
    save_path = "temp.jpg"  # 一時ファイル名
    cv2.imwrite(save_path, result_img)

    return save_path

def main():
    st.title("YOLOv8 姿勢推定")
    uploaded_file = st.file_uploader("画像を選択してください", type=["png", "jpg", "jpeg"])

    model = load_model(MODEL_PATH)

    if uploaded_file is not None:
        # ファイルをNumPy配列に変換
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # 画像処理
        result_path = process_image(img, model)

        # 画像を表示
        st.image(result_path, caption="姿勢推定結果", use_column_width=True)

        # ダウンロードボタン
        with open(result_path, "rb") as f:
            download_button = st.download_button(
                label="結果をダウンロード",
                data=f,
                file_name="pose_estimation.jpg"
            )

if __name__ == "__main__":
    main()
