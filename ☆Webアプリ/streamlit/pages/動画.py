import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# Google ドライブ API 認証情報
credentials = Credentials.from_service_account_file(
    '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json',
    scopes=['https://www.googleapis.com/auth/drive']
)

drive_service = build('drive', 'v3', credentials=credentials)

# 動画をGoogleドライブのフォルダにアップロードする関数
def upload_video_to_folder(folder_id, video_file):
    file_metadata = {
        'name': video_file.name,
        'parents': [folder_id]
    }
    media = MediaIoBaseUpload(video_file, mimetype='video/mp4')  # 動画のMIMEタイプを適切に指定してください
    drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

# メイン処理https://drive.google.com/drive/folders/1oEyH8MMILXXDyXxbOEGPkQK_fzARbPVF?usp=sharing
def main():
    folder_id = '1oEyH8MMILXXDyXxbOEGPkQK_fzARbPVF'
    
    st.title('簡易な動画アップロード')

    # 動画をアップロードする
    uploaded_file = st.file_uploader("動画をアップロードしてください", type=['mp4', 'avi', 'mov'])
    if uploaded_file is not None:
        try:
            upload_video_to_folder(folder_id, uploaded_file)
            st.success("動画が正常にアップロードされました。")
        except Exception as e:
            st.error(f'動画のアップロード中にエラーが発生しました: {e}')

if __name__ == '__main__':
    main()
