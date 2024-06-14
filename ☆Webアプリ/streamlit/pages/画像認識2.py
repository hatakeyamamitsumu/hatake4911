import streamlit as st
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image

# MobileNetV2モデルをロードする
model = MobileNetV2(weights='imagenet')

st.title('MobileNetV2 Image Classification')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を表示する
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image.', use_column_width=True)
    st.write("ファイル名は英語")
    # 画像を処理して、モデルで分類する
    st.write("Classifying...")
    
    # 画像をリサイズしてnumpy配列に変換する
    img_resized = img.resize((224, 224))
    x = image.img_to_array(img_resized)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    # 画像をモデルで分類する
    preds = model.predict(x)
    
    # 結果をデコードして表示する
    predictions = decode_predictions(preds, top=3)[0]
    st.write('Predicted:')
    for pred in predictions:
        st.write(f"{pred[1]}: {pred[2]*100:.2f}%")
