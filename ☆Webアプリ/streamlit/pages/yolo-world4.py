import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np
# 画像サイズを調整する例

# モデルの読み込み
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt') # モデルのパスを適宜変更

def detect_objects(img, model, conf_thres=0.5):
    """物体検出を行う関数"""
    try:
        results = model(img[None, ...], conf=conf_thres)
        annotated_img = results[0].plot()
        return annotated_img
    except Exception as e:
        st.error(f"物体検出中にエラーが発生しました: {e}")
        return None

# Streamlitアプリのレイアウト
st.title("YOLOv8 物体検出アプリ")

# カメラの使用を選択
use_camera = st.checkbox("カメラを使用する")

if use_camera:
    # カメラキャプチャ
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("カメラが開けません")
    else:
        # 撮影ボタン
        if st.button('写真を撮る'):
            ret, frame = cap.read()
            if not ret:
                st.error("カメラから画像を取得できませんでした。")
            else:
                # 物体検出
                result_img = detect_objects(frame, model)
                # 結果を表示
                if result_img is not None:
                    rgb_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                    st.image(rgb_img, channels="RGB", use_column_width=True)
        cap.release()
else:
    # 画像アップロード
    picture = st.camera_input("写真を撮ってください")
    if picture:
        # OpenCVで画像を読み込む
        byte_arr = np.frombuffer(picture.read(), np.uint8)
        cv_image = cv2.imdecode(byte_arr, cv2.IMREAD_COLOR)

        # 物体検出
        result_img = detect_objects(cv_image, model)

        # 画像を表示
        if result_img is not None:
            rgb_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            st.image(rgb_img, channels="RGB", use_column_width=True)

        # 画像を保存し、ダウンロードボタンを表示
        cv2.imwrite("captured_image.jpg", cv_image)
        with open("captured_image.jpg", "rb") as file:
            st.download_button(
                label="画像をダウンロード",
                data=file,
                file_name="captured_image.jpg",
                mime="image/jpeg"
            )
