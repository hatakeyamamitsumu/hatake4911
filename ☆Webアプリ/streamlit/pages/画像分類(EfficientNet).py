import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0, preprocess_input
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np

# EfficientNetB0モデルをロードする
model = EfficientNetB0(weights='imagenet')

# Streamlitアプリケーションのタイトルを設定する
st.title('EfficientNetB0 Image Classification')

# 画像のアップロード用のファイルアップローダーを追加する
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# アップロードされた画像がある場合は、画像を表示し、分類を行う
if uploaded_file is not None:
    # 画像を表示する
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image.', use_column_width=True)
    
    # 画像をモデルに合わせて処理する
    img = img.resize((224, 224))  # EfficientNetB0は画像サイズ224x224を期待することが多い
    
    # 画像をnumpy配列に変換し、前処理を行う
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    # 画像をモデルで分類する
    preds = model.predict(x)
    
    # 分類結果をデコードして表示する
    decoded_preds = tf.keras.applications.efficientnet.decode_predictions(preds, top=3)[0]
    
    st.write('Predicted:')
    for i, (imagenet_id, label, score) in enumerate(decoded_preds):
        st.write(f"{label}: {score*100:.2f}%")
