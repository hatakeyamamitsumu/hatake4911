import streamlit as st
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from PIL import Image

# データセットのパスを変更する必要がある場合は、以下のパスを調整してください。
train_path = "/mount/src/hatake4911/tree/main/☆Webアプリ/画像/dataset/train"
test_path = "/mount/src/hatake4911/tree/main/☆Webアプリ/画像/dataset/test"

# 学習用データ
train_datagen = ImageDataGenerator(rescale=1./255)
train_set = train_datagen.flow_from_directory(
    train_path,
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',
    classes=['CAR', 'SHIP']
)

# テスト用データ
test_datagen = ImageDataGenerator(rescale=1./255)
test_set = test_datagen.flow_from_directory(
    test_path,
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',
    classes=['CAR', 'SHIP']
)

# モデルの構築
model = keras.Sequential([
    Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(units=128, activation='relu'),
    Dense(units=2, activation='softmax')
])

# モデルのコンパイル
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 学習部分をコメントアウトして、エラーの詳細を確認する
try:
    # 学習
    # model.fit(
    #     train_set,
    #     steps_per_epoch=len(train_set),
    #     epochs=20,
    #     validation_data=test_set,
    #     validation_steps=len(test_set)
    # )
    
    # 学習済みモデルをロードする場合は、以下を使用
    # model.load_weights('path_to_saved_model_weights.h5')
    
    st.title("Car vs Ship Image Classifier")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.write("Classifying...")
    
        img = img.resize((64, 64))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
    
        # 結果を出力する
        prediction = model.predict(img_array)
        car_probability = prediction[0][0]
        ship_probability = prediction[0][1]
    
        st.write('Prediction:', prediction)
        st.write('Image is class CAR with probability:', round(car_probability * 100, 5))
        st.write('Image is class SHIP with probability:', round(ship_probability * 100, 5))
except Exception as e:
    st.error(f"An error occurred: {e}")
