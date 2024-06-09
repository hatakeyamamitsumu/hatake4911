import os
import numpy as np
import cv2
import streamlit as st
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Activation
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image

# データセットのパスを指定
dataset_path = '/mount/src/hatake4911/☆Webアプリ/画像/dataset' # ここをデータセットのパスに変更
classes = ['cat', 'dog']
IMG_SIZE = 64

# モデルの作成とトレーニング
data = []
labels = []

# 画像データを読み込む
for c in classes:
    path = os.path.join(dataset_path, c)
    if not os.path.exists(path):
        print(f"Directory {path} does not exist")
        continue

    for img in os.listdir(path):
        try:
            img_path = os.path.join(path, img)
            print(f"Trying to read image: {img_path}")
            image = cv2.imread(img_path)
            if image is None:
                print(f"Failed to read {img_path}")
                continue

            image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
            data.append(image)
            labels.append(classes.index(c))
            print(f"Loaded {img_path}")
        except Exception as e:
            print(f"Error reading {img_path}: {e}")

if len(data) == 0 or len(labels) == 0:
    raise ValueError("No images were loaded. Check your dataset paths and image files.")

data = np.array(data)
labels = np.array(labels)

# データをシャッフルする
idx = np.arange(data.shape[0])
np.random.shuffle(idx)
data = data[idx]
labels = labels[idx]

# データをトレーニング用と検証用に分割する
num_samples = len(data)
num_train = int(num_samples * 0.8)
x_train = data[:num_train]
y_train = labels[:num_train]
x_val = data[num_train:]
y_val = labels[num_train:]

# 画像データの正規化
x_train = x_train / 255.0
x_val = x_val / 255.0

# ラベルをone-hotエンコーディングに変換する
y_train = to_categorical(y_train)
y_val = to_categorical(y_val)

# モデルを構築する
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dense(2))
model.add(Activation('softmax'))

# モデルをコンパイルする
from tensorflow.keras.optimizers import Adam
optimizer = Adam(learning_rate=0.0001)
model.compile(loss='categorical_crossentropy',
              optimizer=optimizer,
              metrics=['accuracy'])

# 早期停止の導入
from tensorflow.keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# モデルをトレーニングする
model.fit(x_train, y_train, epochs=12, batch_size=32, validation_data=(x_val, y_val), callbacks=[early_stopping])

# Streamlitの設定
st.title("Cat vs Dog 画像判定")
st.write("データセットは64*64にリサイズしてあります")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")

    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # 結果を出力する
    prediction = model.predict(img_array)
    cat_probability = prediction[0][0]
    dog_probability = prediction[0][1]

    st.write('Prediction:', prediction)
    st.write('Image is class CAT with probability:', round(cat_probability * 100, 5))
    st.write('Image is class DOG with probability:', round(dog_probability * 100, 5))
