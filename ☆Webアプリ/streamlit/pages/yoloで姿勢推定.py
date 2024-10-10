


import streamlit as st
from ultralytics import YOLOWorld
import numpy as np


# モデルのロード
model = YOLOWorld("/mount/src/hatake4911/☆Webアプリ/その他重要ファイル/yolo11n-pose.pt")  # 姿勢推定モデル

# タイトル設定
st.title("YOLOによる姿勢推定アプリ")

# 画像アップロード
uploaded_file = st.file_uploader("画像を選択してください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    try:
        # 画像の読み込み
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # 推論実行
        results = model(img)

        # 推論結果の表示
        # results.print()  # 推論結果の詳細を表示
        # results.show()  # 画像上に結果を可視化

        # 推論結果から画像を取得し、Streamlitで表示
        if len(results.xyxy) > 0:
            # 検出結果がある場合
            img = results.plot()[0]  # 最初の検出結果の画像を取得
            st.image(img)
        else:
            # 検出結果がない場合
            st.write("人物が検出されませんでした")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
