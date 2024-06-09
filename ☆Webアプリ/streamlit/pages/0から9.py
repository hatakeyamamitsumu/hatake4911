import numpy as np
import streamlit as st
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image

# データセットのロード
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)
x_train, x_test = x_train / 255.0, x_test / 255.0

# ラベルをone-hotエンコーディングに変換
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# データ拡張の設定
datagen = ImageDataGenerator(
    rotation_range=10,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1
)
datagen.fit(x_train)

# モデルの構築
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

# モデルのコンパイル
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# モデルのトレーニング
model.fit(datagen.flow(x_train, y_train, batch_size=32), epochs=20, validation_data=(x_test, y_test))

# Streamlitの設定
st.title("MNIST Handwritten Digit Classification")
st.write("Upload a handwritten digit image (28x28 pixels) to classify it.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("L")  # 画像をグレースケールに変換
    img = img.resize((28, 28))  # 画像を28x28にリサイズ
    img_array = np.array(img)  # 画像をnumpy配列に変換
    img_array = img_array / 255.0  # 画像を正規化
    img_array = np.expand_dims(img_array, axis=-1)  # チャンネル次元を追加
    img_array = np.expand_dims(img_array, axis=0)  # バッチ次元を追加

    st.image(img, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")

    # 予測
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]

    st.write('Prediction:', prediction)
    st.write('The uploaded image is classified as digit:', predicted_class)
