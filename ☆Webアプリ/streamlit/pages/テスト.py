

         
import streamlit as st
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision_v1 import AnnotateFileResponse

# Google Vision API クライアントのセットアップ
def get_vision_client():
    creds = service_account.Credentials.from_service_account_file(
        '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json'
    )
    return vision.ImageAnnotatorClient(credentials=creds)

# OCR処理を行う関数
def perform_ocr(image_path, vision_client):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
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
    # 一時ファイルに保存
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.read())
    
    # OCRを実行
    vision_client = get_vision_client()
    ocr_result = perform_ocr("temp_image.jpg", vision_client)
    
    # 結果を表示
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    st.text_area("Extracted Text", ocr_result)

    # 一時ファイルを削除
    os.remove("temp_image.jpg")
