import streamlit as st
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
import io

# Google ドライブ API 認証情報　https://drive.google.com/drive/folders/1BIEdWNQ1Iw0nEqf8OpGZXDywXFBiQueN?usp=drive_link
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '/mount/src/hatake4911/☆Webアプリ/秘密鍵/gspread-test-421301-6cd8b0cc0e27.json', 
    ['https://www.googleapis.com/auth/drive']
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

# メイン処理
def main():
    st.title('Googleドライブ内の画像を表示する')

    # フォルダIDの入力
    #folder_id = st.text_input('Googleドライブ内のフォルダIDを入力してください')
    folder_id = '1BIEdWNQ1Iw0nEqf8OpGZXDywXFBiQueN'
    if folder_id:
        try:
            images = get_images_from_folder(folder_id)
            if images:
                display_images(images)
            else:
                st.warning('指定されたフォルダ内に画像が見つかりませんでした。')
        except Exception as e:
            st.error(f'エラーが発生しました: {e}')

if __name__ == '__main__':
    main()
