import numpy as np
import streamlit as st
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical
from PIL import Image

# データセットのロード
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# ラベルをone-hotエンコーディングに変換
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# モデルの構築
model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

# モデルのコンパイル
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# モデルのトレーニング
model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# Streamlitの設定
st.title("MNIST Handwritten Digit Classification")
st.write("Upload a handwritten digit image (28x28 pixels) to classify it.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("L")  # 画像をグレースケールに変換
    img = img.resize((28, 28))  # 画像を28x28にリサイズ
    img_array = np.array(img)  # 画像をnumpy配列に変換
    img_array = img_array / 255.0  # 画像を正規化
    img_array = np.expand_dims(img_array, axis=0)  # バッチ次元を追加

    st.image(img, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")

    # 予測
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]

    st.write('Prediction:', prediction)
    st.write('The uploaded image is classified as digit:', predicted_class)
