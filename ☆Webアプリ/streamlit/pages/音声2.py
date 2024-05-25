import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import io

# Google ドライブ API 認証情報
credentials = Credentials.from_service_account_info(
    st.secrets["google"],
    scopes=['https://www.googleapis.com/auth/drive']
)

drive_service = build('drive', 'v3', credentials=credentials)

# Google ドライブ内の特定のフォルダから音声ファイルを検索する関数
def search_audio_in_folder(folder_id):
    results = drive_service.files().list(q=f"'{folder_id}' in parents and mimeType='audio/mpeg'",
                                         fields="files(id, name)").execute()
    return results.get('files', [])

# 音声ファイルをGoogleドライブのフォルダにアップロードする関数
def upload_audio_to_folder(folder_id, audio_file):
    file_metadata = {
        'name': audio_file.name,
        'parents': [folder_id]
    }
    media = MediaIoBaseUpload(audio_file, mimetype='audio/mpeg')  # 音声のMIMEタイプを適切に指定してください
    drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

# Google ドライブから音声ファイルをダウンロードする関数
def download_audio(audio_id):
    request = drive_service.files().get_media(fileId=audio_id)
    downloaded_audio = io.BytesIO()
    downloader = MediaIoBaseDownload(downloaded_audio, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    downloaded_audio.seek(0)
    return downloaded_audio

# メイン処理
def main():
    folder_id = '1jGk6GIRRW465MPEJCP-mZC8csMegXcsy'
    
    st.title('音声アップロードと再生')

    # 音声ファイルをアップロードする
    uploaded_file = st.file_uploader("音声ファイルをアップロードしてください", type=['mp3', 'wav', 'ogg'])
    if uploaded_file is not None:
        try:
            upload_audio_to_folder(folder_id, uploaded_file)
            st.success("音声ファイルが正常にアップロードされました。")
        except Exception as e:
            st.error(f'音声ファイルのアップロード中にエラーが発生しました: {e}')

    # 指定されたフォルダ内の音声ファイルを検索して表示
    audios = search_audio_in_folder(folder_id)
    if audios:
        st.header('音声再生')
        audio_names = [audio
