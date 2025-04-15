import numpy as np
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input, decode_predictions
from keras.preprocessing import image
import streamlit as st
from PIL import Image
import requests
from translate import Translator

# Translatorの設定
translator = Translator(to_lang="ja")

# Streamlitのタイトル
st.title("VGG16を使用した画像認識")

# 画像をアップロードするためのファイルアップローダー
uploaded_file = st.file_uploader("jpg画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を表示
    img = Image.open(uploaded_file)
    img = img.resize((224, 224))
    st.image(img, caption="アップロードされた画像", use_column_width=True)

    # 画像を配列に変換
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # VGG16モデルをロード
    model = VGG16(weights='imagenet')

    # 画像を予測
    predictions = model.predict(img_array)

    # 予測結果をデコード
    decoded_predictions = decode_predictions(predictions, top=3)[0]

    # 予測結果を表示
    st.write("予測結果:")
    for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
        label_ja = translator.translate(label)
        st.write(f"{i+1}: {label_ja} ({label}): {score*100:.2f}%")

# サイドバーに情報を表示
st.sidebar.title("About")
st.sidebar.info("これはStreamlitとVGG16を使用したシンプルな画像認識アプリです。")
