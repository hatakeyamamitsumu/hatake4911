import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import time

# モデルのパス
MODEL_PATH = '/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolo11s-pose.pt'  # 自分のモデルのパスに置き換えてください

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

# カメラキャプチャの開始
cap = cv2.VideoCapture(0)

# 画像を自動で取得するためのボタン
if st.button("自動撮影を開始"):
    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("カメラ映像の取得に失敗しました")
            break

        # 推論
        results = model(frame)

        # キーポイントと骨格を描画
        for result in results:
            if result.keypoints is not None:
                keypoints = result.keypoints.xy
                draw_keypoints_and_skeleton(frame, keypoints)

        # 画像を表示
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, channels="RGB")

        # 3秒待機
        time.sleep(10)

# 処理終了
cap.release()
