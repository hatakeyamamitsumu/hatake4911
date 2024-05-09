import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Google ドライブ API 認証情報
credentials = Credentials.from_service_account_file(
    '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json',
    scopes=['https://www.googleapis.com/auth/drive']
)

drive_service = build('drive', 'v3', credentials=credentials)

# Google ドライブ内の特定のフォルダから動画を検索する関数
def search_videos_in_folder(folder_id):
    results = drive_service.files().list(q=f"'{folder_id}' in parents and mimeType='video/mp4'",
                                         fields="files(id, name)").execute()
    return results.get('files', [])

# Google ドライブから動画をダウンロードする関数
def download_video(video_id):
    request = drive_service.files().get_media(fileId=video_id)
    downloaded_video = io.BytesIO()
    downloader = MediaIoBaseDownload(downloaded_video, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    downloaded_video.seek(0)
    return downloaded_video

# メイン処理　https://drive.google.com/drive/folders/1oEyH8MMILXXDyXxbOEGPkQK_fzARbPVF?usp=sharing
def main():
    folder_id = '1oEyH8MMILXXDyXxbOEGPkQK_fzARbPVF'
    
    st.title('動画再生')

    # フォルダ内の動画を取得
    videos = search_videos_in_folder(folder_id)
    video_names = [video['name'] for video in videos]

    # 動画を選択
    selected_video_name = st.selectbox("再生する動画を選択してください", video_names)

    # 選択された動画のIDを取得
    selected_video = [video for video in videos if video['name'] == selected_video_name][0]
    video_id = selected_video['id']

    # 動画をダウンロードして再生
    st.subheader('選択された動画')
    downloaded_video = download_video(video_id)
    st.video(downloaded_video, format='video/mp4')

if __name__ == '__main__':
    main()
