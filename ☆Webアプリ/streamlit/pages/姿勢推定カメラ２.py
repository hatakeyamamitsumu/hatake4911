import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import time

# モデルのパス
MODEL_PATH = 'yolo11l-pose.pt'

# モデルのロード
model = YOLO(MODEL_PATH)

# キーポイントの接続順序 (骨格の線を描画するためのペア)
skeleton_pairs = [
    (1, 2),  # 両目
    (5, 6), (5, 7), (6, 8), (7, 9),
    (8, 10), (11, 13), (11, 12),
    (12, 14), (13, 15), (14, 16)
]

# キーポイントと骨格を描画する関数
def draw_keypoints_and_skeleton(frame, keypoints):
    for keypoint in keypoints:
        for x, y in keypoint:
            if x > 0 and y > 0:
                cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)
        for pair in skeleton_pairs:
            x1, y1 = keypoint[pair[0]]
            x2, y2 = keypoint[pair[1]]
            if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

# Streamlit UIの設定
st.title("リアルタイム姿勢推定")

# フレーム表示用
frame_window = st.image([])  # 空のイメージを作成

# カメラ入力をループして連続取得
while True:
    picture = st.camera_input("カメラ映像を取得中...")

    if picture:
        # OpenCVで画像を読み込む
        byte_arr = np.frombuffer(picture.read(), np.uint8)
        cv_image = cv2.imdecode(byte_arr, cv2.IMREAD_COLOR)

        # 推論
        results = model(cv_image)

        # キーポイントと骨格を描画
        for result in results:
            if result.keypoints is not None:
                keypoints = result.keypoints.xy
                draw_keypoints_and_skeleton(cv_image, keypoints)

        # 画像を表示
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        frame_window.image(cv_image)  # ここでリアルタイムでフレームを更新

        time.sleep(0.03)  # 30ミリ秒の遅延を追加
