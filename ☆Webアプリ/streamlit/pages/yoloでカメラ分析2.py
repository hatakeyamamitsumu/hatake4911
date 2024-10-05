import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np
import os

# モデルの読み込み (パスを適宜変更)
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolov8s.pt')

# 画像を保存するディレクトリ
save_dir = 'captured_images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 画像保存用のリスト
image_paths = []

# カメラ入力
picture = st.camera_input("写真を撮ってください")

if picture:
    # OpenCVで画像を読み込む
    byte_arr = np.frombuffer(picture.read(), np.uint8)
    cv_image = cv2.imdecode(byte_arr, cv2.IMREAD_COLOR)

    # 画像を表示
    st.image(cv_image, channels="BGR")

    # 画像を保存
    filename = f'captured_image_{len(image_paths)}.jpg'
    filepath = os.path.join(save_dir, filename)
    cv2.imwrite(filepath, cv_image)
    image_paths.append(filepath)

    # 物体検出を実行
    processed_image = detect_objects(filepath, model)

    # 結果を表示
    if processed_image is not None:
        # BGRをRGBに変換
        rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        st.image(rgb_image, channels="RGB", use_column_width=True)

def detect_objects(image_path, model):
    """
    物体検出を行う関数

    Args:
        image_path: 画像のファイルパス
        model: YOLOv8モデル

    Returns:
        処理済みの画像 (BGR形式)
    """

    try:
        # 画像を読み込む
        img = cv2.imread(image_path)

        # 物体検出
        results = model.predict(source=img)
        annotated_img = results[0].plot()

        return annotated_img
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        return None

# 追加機能の例 (閾値のスライダー)
confidence_threshold = st.slider("信頼度閾値", min_value=0.0, max_value=1.0, value=0.5)
# モデルの再初期化 (閾値変更時に必要)
model.conf = confidence_threshold
