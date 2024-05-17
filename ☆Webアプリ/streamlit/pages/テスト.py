
       
import streamlit as st
from google.oauth2 import service_account
from google.cloud import vision

# Google Vision API クライアントのセットアップ
def get_vision_client():
    creds = service_account.Credentials.from_service_account_file(
         '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json'
    )
    return vision.ImageAnnotatorClient(credentials=creds)

# OCR処理を行う関数
def perform_ocr(image_content, vision_client):
    image = vision.Image(content=image_content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    else:
        return "No text found"

# Streamlitアプリケーション
st.title("Image OCR with Google Cloud Vision")

uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_content = uploaded_file.read()
    st.image(image_content, caption='Uploaded Image.', use_column_width=True)
    
    vision_client = get_vision_client()
    text = perform_ocr(image_content, vision_client)
    
    st.text_area("Extracted Text", text)
