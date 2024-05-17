import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.cloud import vision

# GoogleドライブAPIの認証情報を取得する関数
def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json',
        scopes=['https://www.googleapis.com/auth/drive']
    )
    return build('drive', 'v3', credentials=creds)

# Google Cloud Vision APIのクライアントを取得する関数
def get_vision_client():
    creds = service_account.Credentials.from_service_account_file(
        '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json'
    )
    return vision.ImageAnnotatorClient(credentials=creds)

# 画像をGoogleドライブにアップロードする関数
def upload_image_to_drive(image_file, folder_id, drive_service):
    file_metadata = {
        'name': image_file.name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(image_file.name, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# Googleドキュメントを作成し、画像を挿入してOCRを実行する関数
def perform_ocr_on_document(image_id, vision_client):
    document = {
        'title': 'OCR Document'
    }
    doc = drive_service.files().create(body=document, media_body=None).execute()
    document_id = doc.get('id')

    batch = vision.BatchAnnotateImagesRequest()
    batch.requests = [{
        'image': {
            'source': {
                'imageUri': f'https://drive.google.com/uc?id={image_id}'
            }
        },
        'features': [
            {'type': 'DOCUMENT_TEXT_DETECTION'}
        ]
    }]
    response = vision_client.batch_annotate_images(requests=batch)
    full_text = response.responses[0].full_text_annotation.text

    return full_text

# Streamlitアプリケーション
st.title("OCR on Image Uploaded to Google Drive")

uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
if uploaded_file:
    folder_id = "1GOO5qF34z32MyAYSr4lUBLDV7rnYcRYS"  # Googleドライブ内のフォルダID
    drive_service = get_drive_service()
    image_id = upload_image_to_drive(uploaded_file, folder_id, drive_service)

    vision_client = get_vision_client()
    ocr_result = perform_ocr_on_document(image_id, vision_client)

    st.write("OCR Result:")
    st.write(ocr_result)
