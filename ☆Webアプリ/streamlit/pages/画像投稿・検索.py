import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from PIL import Image
import io

# Google ドライブ API 認証情報
credentials = Credentials.from_service_account_file(
    '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json',
    scopes=['https://www.googleapis.com/auth/drive']
)

drive_service = build('drive', 'v3', credentials=credentials)

# フォルダ内の画像を取得する関数
def get_images_from_folder(folder_id):
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/'",
        fields='files(id, name)'
    ).execute()
    images = results.get('files', [])
    return images

# フォルダ内の画像を表示する関数
def display_images(images):
    for image in images:
        image_id = image['id']
        file = drive_service.files().get_media(fileId=image_id)
        image_data = io.BytesIO(file.execute())
        img = Image.open(image_data)
        st.image(img, caption=image['name'], use_column_width=True)

#フォルダ内の特定のファイル名を持つ画像を取得する関数
def search_images_by_filename(folder_id, filename):
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/' and name contains '{filename}'",
        fields='files(id, name)'
    ).execute()
    images = results.get('files', [])
    return images

# 画像をGoogleドライブのフォルダにアップロードする関数
def upload_image_to_folder(folder_id, image_file):
    file_metadata = {
        'name': image_file.name,
        'parents': [folder_id]
    }
    media = MediaIoBaseUpload(image_file, mimetype='image/jpeg')  # 画像のMIMEタイプを適切に指定してください
    drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

# メイン処理
def main():
    st.title('Googleドライブ内の画像を表示する')

    # フォルダIDの入力
    #folder_id = st.text_input('Googleドライブ内のフォルダIDを入力してください')
    folder_id ='1BIEdWNQ1Iw0nEqf8OpGZXDywXFBiQueN'
    if folder_id:
        try:
            # ファイル名を検索するための入力欄
            search_query = st.text_input("検索するファイル名を入力してください：")
            
            images = []
            if search_query:
                images = search_images_by_filename(folder_id, search_query)
            else:
                images = get_images_from_folder(folder_id)
            
            if images:
                display_images(images)
            elif search_query:
                st.warning('指定された条件に一致する画像が見つかりませんでした。')
        except Exception as e:
            st.error(f'エラーが発生しました: {e}')
    else:
        st.warning('Googleドライブ内のフォルダIDを入力してください。')

    # 画像をアップロードする
    uploaded_file = st.file_uploader("画像をアップロードしてください（アップロードした画像は削除できません）", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        try:
            upload_image_to_folder(folder_id, uploaded_file)
            st.success("画像が正常にアップロードされました。")
        except Exception as e:
            st.error(f'画像のアップロード中にエラーが発生しました: {e}')

if __name__ == '__main__':
    main()
