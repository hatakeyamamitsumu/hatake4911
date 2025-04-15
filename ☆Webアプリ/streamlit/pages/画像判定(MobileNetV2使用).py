import streamlit as st
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image
from translate import Translator

# MobileNetV2モデルをロードする
model = MobileNetV2(weights='imagenet')

# Translatorの設定
translator = Translator(to_lang="ja")

st.title('MobileNetV2を使った画像分類')
st.write("jpgファイルをアップロードしてください")
uploaded_file = st.file_uploader("画像ファイルをアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を表示する
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image.', use_column_width=True)

    # 画像を処理して、モデルで分類する
    st.write("分類結果")
    
    # 画像をリサイズしてnumpy配列に変換する
    img_resized = img.resize((224, 224))
    x = image.img_to_array(img_resized)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    # 画像をモデルで分類する
    preds = model.predict(x)
    
    # 結果をデコードして表示する
    predictions = decode_predictions(preds, top=3)[0]
    st.write('予測結果:')
    for pred in predictions:
        label_en = pred[1]
        label_ja = translator.translate(label_en)
        st.write(f"{label_ja} ({label_en}): {pred[2]*100:.2f}%")
