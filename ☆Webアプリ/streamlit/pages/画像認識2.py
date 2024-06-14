import streamlit as st
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image

# VGG16モデルをロードする
model = VGG16(weights='imagenet')

st.title('VGG16 Image Classification')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を表示する
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image.', use_column_width=True)
    
    # 画像を処理して、モデルで分類する
    st.write("Classifying...")
    
    # 画像をリサイズする
    img = img.resize((224, 224))
    
    # 画像をnumpy配列に変換する
    x = image.img_to_array(img)
    
    # 画像の次元を(1, 224, 224, 3)に拡張する
    x = np.expand_dims(x, axis=0)
    
    # 画像を前処理する
    x = preprocess_input(x)
    
    # 画像をモデルで分類する
    preds = model.predict(x)
    
    # 結果をデコードして表示する
    predictions = decode_predictions(preds, top=3)[0]
    st.write('Predicted:')
    for pred in predictions:
        st.write(f"{pred[1]}: {pred[2]*100:.2f}%")

