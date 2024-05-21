import streamlit as st
import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from PIL import Image
import numpy as np
import tensorflow as tf

# Google Drive API認証とクライアント作成
def authenticate_gdrive():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build("drive", "v3", credentials=credentials)
    return service

# 特定のGoogle Driveフォルダ内のファイルをリストする
def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query).execute()
    return results.get('files', [])

# Google Driveからファイルをダウンロードする
def download_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    file_io = io.BytesIO()
    downloader = googleapiclient.http.MediaIoBaseDownload(file_io, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    file_io.seek(0)
    return file_io

# 事前訓練済みの画像分類モデルをロードする（例：MobileNetV2）
def load_model():
    model = tf.keras.applications.mobilenet_v2.MobileNetV2(weights="imagenet")
    return model

# 画像を分類用に前処理する
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image)
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image

# 画像を分類する
def classify_image(model, image):
    predictions = model.predict(image)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0][0]
    return decoded_predictions

# Streamlitアプリケーション
def main():
    st.title("Google Drive 画像分類アプリ")

    folder_a_id = st.text_input("人物AのフォルダIDを入力してください:", "")
    folder_b_id = st.text_input("人物BのフォルダIDを入力してください:", "")
    
    if st.button("分類を開始"):
        if folder_a_id and folder_b_id:
            service = authenticate_gdrive()

            st.write("人物Aの写真を取得しています...")
            files_a = list_files_in_folder(service, folder_a_id)
            st.write(f"人物Aのフォルダに {len(files_a)} 枚の写真があります。")

            st.write("人物Bの写真を取得しています...")
            files_b = list_files_in_folder(service, folder_b_id)
            st.write(f"人物Bのフォルダに {len(files_b)} 枚の写真があります。")

            # モデルのロード
            model = load_model()

            st.write("人物Aの写真を分類しています...")
            for file in files_a:
                st.write(f"ファイル: {file['name']}")
                file_io = download_file(service, file['id'])
                image = Image.open(file_io)
                st.image(image, caption=file['name'])

                # 画像を前処理して分類
                preprocessed_image = preprocess_image(image)
                prediction = classify_image(model, preprocessed_image)
                st.write(f"予測結果: {prediction[1]} ({prediction[2]*100:.2f}%)")

            st.write("人物Bの写真を分類しています...")
            for file in files_b:
                st.write(f"ファイル: {file['name']}")
                file_io = download_file(service, file['id'])
                image = Image.open(file_io)
                st.image(image, caption=file['name'])

                # 画像を前処理して分類
                preprocessed_image = preprocess_image(image)
                prediction = classify_image(model, preprocessed_image)
                st.write(f"予測結果: {prediction[1]} ({prediction[2]*100:.2f}%)")

if __name__ == "__main__":
    main()
