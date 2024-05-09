import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os


# Google ドライブ API 認証情報
credentials = Credentials.from_service_account_file(
    os.environ['GOOGLE_SERVICE_ACCOUNT_KEY_FILE'],
    scopes=['https://www.googleapis.com/auth/drive'],
)

drive_service = build('drive', 'v3', credentials=credentials)


# 動画を Google ドライブのフォルダにアップロードする関数
def upload_video_to_folder(folder_id, video_file):
    file_metadata = {
        'name': video_file.name,
        'parents': [folder_id],
    }
    media = MediaFileUpload(video_file.name, mimetype='video/mp4')  # 動画の MIME タイプを適切に指定してください

    try:
        drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
        ).execute()
    except Exception as e:
        # エラー内容を詳しく取得
        error_details = e.args[0]
        if 'message' in error_details:
            error_message = error_details['message']
        else:
            error_message = '不明なエラーが発生しました'

        st.error(f'動画 {video_file.name} のアップロード中にエラーが発生しました: {error_message}')


# メイン処理
def main():
    folder_id = '1oEyH8MMILXXDyXxbOEGPkQK_fzARbPVF'

    st.title('簡易な動画アップロード')

    # 動画をアップロードする
    uploaded_files = st.file_uploader("動画をアップロードしてください", type=['mp4', 'avi', 'mov', 'wmv', 'flv', 'mpg', 'mpeg'])
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            try:
                upload_video_to_folder(folder_id, uploaded_file)
                st.success(f"動画 {uploaded_file.name} が正常にアップロードされました。")
            except Exception as e:
                st.error(f'動画 {uploaded_file.name} のアップロード中にエラーが発生しました: {e}')


if __name__ == '__main__':
    main()
