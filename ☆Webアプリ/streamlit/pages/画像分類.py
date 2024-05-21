import streamlit as st
import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PIL import Image
import numpy as np
import tensorflow as tf

# Google Drive API認証とクライアント作成
def authenticate_gdrive():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["'/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json"],
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
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_io.seek(0)
    return file_io

# 事前訓練済みの画像分類モデルをロードする（例：MobileNetV2）
@st.cache(allow_output_mutation=True)
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

# フォルダ内の画像を分類し、予測ラベルのリストを返す
def classify_folder_images(service, folder_id, model):
    files = list_files_in_folder(service, folder_id)
    predictions = []
    for file in files:
        file_io = download_file(service, file['id'])
        image = Image.open(file_io)
        preprocessed_image = preprocess_image(image)
        prediction = classify_image(model, preprocessed_image)
        predictions.append(prediction[1])
    return predictions

# 画像のリストから最も頻繁に出現するラベルを取得する
def get_most_common_label(predictions):
    return max(set(predictions), key=predictions.count)

# Streamlitアプリケーション
def main():
    st.title("Google Drive 画像分類アプリ")

    folder_a_id = st.text_input("人物AのフォルダIDを入力してください:", "")
    folder_b_id = st.text_input("人物BのフォルダIDを入力してください:", "")
    
    if st.button("分類を開始"):
        if folder_a_id and folder_b_id:
            try:
                service = authenticate_gdrive()

                # モデルのロード
                model = load_model()

                st.write("人物Aの写真を分類しています...")
                predictions_a = classify_folder_images(service, folder_a_id, model)
                label_a = get_most_common_label(predictions_a)
                st.write(f"人物Aの最も一般的なラベル: {label_a}")

                st.write("人物Bの写真を分類しています...")
                predictions_b = classify_folder_images(service, folder_b_id, model)
                label_b = get_most_common_label(predictions_b)
                st.write(f"人物Bの最も一般的なラベル: {label_b}")

                st.write("画像をアップロードして判定します")
                uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="アップロードされた画像")

                    # アップロード画像を前処理して分類
                    preprocessed_image = preprocess_image(image)
                    prediction = classify_image(model, preprocessed_image)
                    st.write(f"アップロード画像の予測結果: {prediction[1]} ({prediction[2]*100:.2f}%)")

                    # 判定
                    if prediction[1] == label_a:
                        st.write("アップロードされた画像は人物Aに近いです。")
                    elif prediction[1] == label_b:
                        st.write("アップロードされた画像は人物Bに近いです。")
                    else:
                        st.write("アップロードされた画像のラベルは人物Aまたは人物Bのどちらとも一致しません。")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
