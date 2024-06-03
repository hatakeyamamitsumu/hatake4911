from google.oauth2 import service_account
from googleapiclient.discovery import build

# 認証情報のロード
credentials = service_account.Credentials.from_service_account_file(
    'path/to/service_account_credentials.json',
    scopes=['https://www.googleapis.com/auth/drive.readonly'])

# Google ドライブ API のビルド
drive_service = build('drive', 'v3', credentials=credentials)

def download_file(file_id):
    # ファイルのダウンロード
    request = drive_service.files().export_media(fileId=file_id, mimeType='text/plain')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    return fh.getvalue().decode()

# GoogleドキュメントのID
document_id = '1bdkuJ9LqSNqfYA3MeMCHHsXPxLtIlBmPlpMjUBCWuw0'

# ドキュメントからテキストを取得
document_text = download_file(document_id)

# テキストを出力
print(document_text)
