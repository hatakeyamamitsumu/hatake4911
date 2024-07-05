from PIL import Image, ImageDraw, ImageOps
import easyocr
import streamlit as st
import numpy as np

# Streamlitアプリケーションのタイトルと説明
st.title("easyocrを使った簡単な写真の中の文字読み取り")
st.write("jpgファイルをアップロードしてください")

# easyocrの初期化
reader = easyocr.Reader(['ja', 'en'])

# 画像のアップロード
selected_image = st.file_uploader('upload image', type='jpg')

# 画像表示用の空のコンポーネント
original_image = st.empty()
result_image = st.empty()

if selected_image is not None:
    # アップロードされた画像を表示
    original_image.image(selected_image)

    # PILで画像を開く
    pil_image = Image.open(selected_image)

    # 画像の前処理と二値化処理
    # 例: リサイズと二値化

    pil_image = ImageOps.grayscale(pil_image)  # グレースケールに変換
    threshold = 127  # 二値化の閾値
    pil_image = pil_image.point(lambda p: p > threshold and 255)  # 二値化

    # OCRでテキストを読み取る
    result = reader.readtext(np.array(pil_image))

    # 結果を描画するための準備
    draw = ImageDraw.Draw(pil_image)

    # 結果を処理して表示
    for bbox, text, score in result:
        # bboxをタプルに変換して矩形を描画
        bbox = tuple(map(tuple, bbox))
        draw.rectangle(bbox, outline="blue", width=3)
        # テキストと信頼性スコアを表示
        st.write(f"テキスト: {text}, 信頼性: {score}")

    # 結果画像を表示
    result_image.image(pil_image)
