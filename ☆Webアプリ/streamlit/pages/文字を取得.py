import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import tempfile

# Streamlit secretsからGoogle Cloudプロジェクトのサービスアカウントキーを読み込む
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
credentials = service_account.Credentials.from_service_account_info(st.secrets["google"], scopes=SCOPES)

# Google Drive APIクライアントを作成
drive_service = build('drive', 'v3', credentials=credentials)

# Google Docs APIクライアントを作成
docs_service = build('docs', 'v1', credentials=credentials)

def upload_file_to_google_drive(file, folder_id):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.getvalue())
        temp_file.flush()

        file_metadata = {
            'name': file.name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(temp_file.name, resumable=True)
        uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return uploaded_file.get('id')

def extract_text_with_google_docs(file_id):
    # Google DocsにインポートしてOCRを実行
    document = docs_service.documents().create(body={
        'title': 'OCR Document'
    }).execute()
    
    # ファイルIDを取得
    doc_id = document.get('documentId')

    # ファイルをインポート
    drive_service.files().copy(fileId=file_id, body={'parents': [doc_id]}).execute()

    # Google Docsの内容を取得
    document = docs_service.documents().get(documentId=doc_id).execute()
    text = ''
    for element in document.get('body').get('content'):
        if 'paragraph' in element:
            for text_run in element['paragraph']['elements']:
                text += text_run['textRun']['content']
    
    return text

def main():
    st.title("Google DriveとGoogle Docsを使用したOCR")
    
    # ファイルアップローダー
    uploaded_file = st.file_uploader("ファイルをアップロードしてください", type=["pdf", "jpg", "png"])
    
    if uploaded_file is not None:
        # ファイルをGoogle Driveの指定フォルダにアップロード
        folder_id = '1GOO5qF34z32MyAYSr4lUBLDV7rnYcRYS'
        file_id = upload_file_to_google_drive(uploaded_file, folder_id)
        
        # Google DocsでOCRを実行
        ocr_text = extract_text_with_google_docs(file_id)
        
        # OCR結果を表示
        st.text_area("OCRで抽出されたテキスト", ocr_text, height=300)

if __name__ == "__main__":
    main()
