import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np

# モデルの読み込み (パスを適宜変更)
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt')

def detect_objects_from_camera(model):
    """
    カメラから画像を取得し、物体検出を行う関数

    Args:
        model: YOLOv8モデル

    Returns:
        処理済みの画像 (BGR形式)
    """

    # カメラキャプチャの設定
    cap = cv2.VideoCapture(0)

    while True:
        # フレームを取得
        ret, frame = cap.read()

        # 物体検出
        results = model.predict(source=frame)
        annotated_frame = results[0].plot()

        # フレームを表示
        cv2.imshow('Object Detection', annotated_frame)

        # 'q'キーを押すと終了
        if cv2.waitKey(1) == ord('q'):
            break

    # カメラを解放
    cap.release()
    cv2.destroyAllWindows()

# Streamlitアプリのレイアウト
st.title("YOLOv8 リアルタイム物体検出アプリ")
st.button("カメラ起動", on_click=detect_objects_from_camera, args=(model,))
