
import streamlit as st
from icrawler.builtin import BingImageCrawler
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 画像をクロールして保存する関数
def crawl_images(keyword, max_num=10):
    save_dir = f"./{keyword}_images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    crawler = BingImageCrawler(storage={"root_dir": save_dir})
    crawler.crawl(keyword=keyword, max_num=max_num)
    
    # ダウンロードした画像のパスを取得
    image_paths = []
    for root, dirs, files in os.walk(save_dir):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png')):
                image_paths.append(os.path.join(root, file))
    return image_paths

# Google Driveに画像をアップロードする関数
def upload_to_drive(images, folder_id):

    )
    # Google ドライブ API 認証情報
creds = Credentials.from_service_account_file(
    '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json',
    st.secrets['https://www.googleapis.com/auth/drive']
    drive_service = build("drive", "v3", credentials=creds)
    
    for image in images:
        file_metadata = {
            "name": os.path.basename(image),
            "parents": [folder_id]
        }
        media = MediaFileUpload(image, resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        st.write(f"{image} を Google Drive にアップロードしました。ID: {file.get('id')}")

# Streamlitアプリ
st.title("画像クローリング・表示")

keyword = st.text_input("キーワードを入力してください:")
max_images = st.number_input("取得する画像の枚数を入力してください:", min_value=1, max_value=100, value=10)

if st.button("クローリングして表示"):
    if keyword:
        st.write(f"{keyword} に関連する画像をクローリングしています...")
        images = crawl_images(keyword, max_num=max_images)
        
        if images:
            st.write("取得した画像:")
            for img_path in images:
                st.image(img_path)
            
            # Google Drive フォルダーIDが提供された場合、画像を Google Drive にアップロードする
            folder_id = "1wXcqvpc2EkJ84adcBMkxBeBv8LdIhhYa"
            if st.button("Google Drive にアップロード"):
                upload_to_drive(images, folder_id)
        else:
            st.write("画像が見つかりませんでした。")
    else:
        st.write("キーワードを入力してください。")
