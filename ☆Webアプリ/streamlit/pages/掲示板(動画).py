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

# Google ドライブ内の特定のフォルダから動画を検索する関数
def search_videos_in_folder(folder_id):
    results = drive_service.files().list(q=f"'{folder_id}' in parents and mimeType='video/mp4'",
                                         fields="files(id, name)").execute()
    return results.get('files', [])

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

# メイン処理
def main():
    folder_id = '1oEyH8MMILXXDyXxbOEGPkQK_fzARbPVF'
    
    st.title('動画アップロードと再生')

    # 動画をアップロードする
    uploaded_file = st.file_uploader("動画をアップロードしてください", type=['mp4', 'avi', 'mov'])
    if uploaded_file is not None:
        try:
            upload_video_to_folder(folder_id, uploaded_file)
            st.success("動画が正常にアップロードされました。")
        except Exception as e:
            st.error(f'動画のアップロード中にエラーが発生しました: {e}')

    # 指定されたフォルダ内の動画を検索して表示

    videos = search_videos_in_folder(folder_id)
    if videos:

        st.header('動画再生')
        video_names = [video['name'] for video in videos]
        selected_video_name = st.selectbox("再生する動画を選択してください", video_names)
        selected_video = [video for video in videos if video['name'] == selected_video_name][0]
        video_id = selected_video['id']
        st.subheader('選択された動画')
        st.write("動画の上で右クリック→名前を付けてビデオを保存　からダウンロードできます")
        downloaded_video = download_video(video_id)
        st.video(downloaded_video, format='video/mp4')

if __name__ == '__main__':
    main()
