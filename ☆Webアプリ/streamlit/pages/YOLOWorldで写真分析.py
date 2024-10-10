import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np

#  モデルの読み込み (パスを適宜変更)
model = YOLOWorld('/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolo11s.pt')

def detect_objects(uploaded_image, model):
 

    try:
        # 画像のデコード
        img = cv2.imdecode(np.frombuffer(uploaded_image.getvalue(), np.uint8), cv2.IMREAD_COLOR)

        # 物体検出
        results = model.predict(source=img)
        annotated_img = results[0].plot()

        return annotated_img
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        return None

# Streamlitアプリのレイアウト
st.title("YOLO 物体検出アプリ")
st.subheader("画像ファイルをアップロードしてください")

uploaded_image = st.file_uploader("", type=['jpg', 'jpeg', 'png'])

if uploaded_image is not None:
    # 物体検出を実行
    processed_image = detect_objects(uploaded_image, model)

    # 結果を表示
    if processed_image is not None:
        # BGRをRGBに変換
        rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        st.image(rgb_image, channels="RGB", use_column_width=True)

# 追加機能の例 (閾値のスライダー)
confidence_threshold = st.slider("信頼度閾値", min_value=0.0, max_value=1.0, value=0.5)
# モデルの再初期化 (閾値変更時に必要)
model.conf = confidence_threshold
