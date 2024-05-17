import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from google.cloud import vision

# Google Drive API Authentication
def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json',
        scopes=['https://www.googleapis.com/auth/drive']
    )
    return build('drive', 'v3', credentials=creds)

# Google Vision API Client
def get_vision_client():
    creds = service_account.Credentials.from_service_account_file(
        '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json'
    )
    return vision.ImageAnnotatorClient(credentials=creds)

# Function to Download Image from Google Drive
def download_image(file_id, drive_service):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# Function to Perform OCR using Google Vision API
def perform_ocr(image_content, vision_client):
    image = vision.Image(content=image_content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    else:
        return "No text found"

# Streamlit Application
st.title("Google Drive OCR with Streamlit")

file_id = st.text_input("Enter the Google Drive file ID of the image:")

if st.button("Perform OCR"):
    if file_id:
        drive_service = get_drive_service()
        vision_client = get_vision_client()
        try:
            image_content = download_image(file_id, drive_service).read()
            st.image(image_content, caption='Uploaded Image.', use_column_width=True)
            text = perform_ocr(image_content, vision_client)
            st.text_area("Extracted Text", text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a Google Drive file ID.")
