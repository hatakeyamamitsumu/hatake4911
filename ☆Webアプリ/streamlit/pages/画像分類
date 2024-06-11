import os
import numpy as np
import streamlit as st
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from PIL import Image

# データセットのパスを指定
dataset_path = '/mount/src/hatake4911/☆Webアプリ/画像/dataset' # ここをデータセットのパスに変更
IMG_SIZE = 224  # MobileNetV2の標準入力サイズに変更
BATCH_SIZE = 32

# データ拡張の設定
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2  # トレーニングデータと検証データに分割
)

train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# MobileNetV2のベースモデルをロードし、学習を無効化
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
base_model.trainable = False

# モデルの構築
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation='relu'),
    Dense(train_generator.num_classes, activation='softmax')
])

# モデルをコンパイル
optimizer = Adam(learning_rate=0.0001)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# 早期停止の導入
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# モデルをトレーニング
model.fit(
    train_generator,
    epochs=20,
    validation_data=validation_generator,
    callbacks=[early_stopping]
)

# Streamlitの設定
st.title("Cat vs Dog 画像判定")
st.write("データセットは224*224にリサイズしてあります")
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
