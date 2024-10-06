import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np

# モデルの読み込み (一度だけロード)
model = YOLO('yolov8s.pt')  # モデルのパスを適宜変更

def detect_objects(uploaded_image, model, conf_thres=0.5):
    """
    物体検出を行う関数

    Args:
        uploaded_image: アップロードされた画像
        model: YOLOモデル
        conf_thres: 信頼度閾値

    Returns:
        処理済みの画像 (BGR形式)
    """

    try:
        # 画像のデコード
        img = cv2.imdecode(np.frombuffer(uploaded_image.getvalue(), np.uint8), cv2.IMREAD_COLOR)

        # 物体検出 (バッチサイズ1で処理)
        results = model(img[None, ...], conf=conf_thres)  # 信頼度閾値を設定

        # 検出結果を画像に重ねる
        annotated_img = results[0].plot()

        return annotated_img
    except cv2.error as e:
        st.error("画像の読み込みに失敗しました。画像形式を確認してください。")
    except Exception as e:
        st.error(f"予期せぬエラーが発生しました: {e}")
        return None

# Streamlitアプリのレイアウト
st.title("YOLOv8 物体検出アプリ")
st.subheader("画像ファイルをアップロードしてください")

uploaded_image = st.file_uploader("", type=['jpg', 'jpeg', 'png'])

if uploaded_image is not None:
    # 信頼度閾値のスライダー
    confidence_threshold = st.slider("信頼度閾値", min_value=0.0, max_value=1.0, value=0.5)

    # 物体検出を実行
    processed_image = detect_objects(uploaded_image, model, confidence_threshold)

    # 結果を表示
    if processed_image is not None:
        # BGRをRGBに変換
        rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        st.image(rgb_image, channels="RGB", use_column_width=True)

