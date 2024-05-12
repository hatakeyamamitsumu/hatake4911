import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
import os
import tempfile
import subprocess

# Google ドライブ API の認証情報を設定
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json'  # Google Cloud Console で取得したサービス アカウント キーの JSON ファイル

# Streamlit アプリのレイアウト
st.title('Google Drive Python Code Runner')

# Google ドライブのファイルを選択
file_id = st.text_input('Enter the Google Drive file ID:')
if file_id:
    # Google ドライブからファイルを取得する関数
    def download_file_from_drive(file_id):
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)

        request = service.files().export_media(fileId=file_id, mimeType='text/plain')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        return fh.getvalue().decode('utf-8')

    # Google ドライブからファイルを取得して一時ファイルに保存
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, 'script.py')
        file_content = download_file_from_drive(file_id)
        with open(temp_file_path, 'w') as f:
            f.write(file_content)

        # 取得した Python スクリプトを実行
        st.write('Running the script...')
        try:
            result = subprocess.run(['python', temp_file_path], capture_output=True, text=True)
            st.write('Output:')
            st.code(result.stdout)
            if result.stderr:
                st.error(result.stderr)
        except Exception as e:
            st.error(f'Error executing the script: {e}')
