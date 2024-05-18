import streamlit as st
from icrawler.builtin import BingImageCrawler
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

# Google Drive認証
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # 認証フローを開始
    drive = GoogleDrive(gauth)
    return drive

# 画像をクロールして保存
def crawl_images(keyword, max_num=10):
    save_dir = f"./{keyword}_images"
    crawler = BingImageCrawler(storage={"root_dir": save_dir})
    crawler.crawl(keyword=keyword, max_num=max_num)
    
    # ダウンロードした画像のパスを取得
    image_paths = []
    for root, dirs, files in os.walk(save_dir):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png')):
                image_paths.append(os.path.join(root, file))
    return image_paths

# Google Driveに画像をアップロード
def upload_images_to_drive(drive, folder_id, image_paths):
    for img_path in image_paths:
        file1 = drive.CreateFile({"parents": [{"id": folder_id}]})
        file1.SetContentFile(img_path)
        file1.Upload()
        os.remove(img_path)  # ローカルから削除

# Streamlitアプリ
st.title("画像クローリング＆Googleドライブアップロード")

keyword = st.text_input("キーワードを入力してください:")
max_images = st.number_input("取得する画像の枚数を入力してください:", min_value=1, max_value=100, value=10)

if st.button("クローリング＆アップロード"):
    if keyword:
        st.write(f"{keyword} に関連する画像をクローリングしています...")
        images = crawl_images(keyword, max_num=max_images)
        st.write("画像をGoogleドライブにアップロードしています...")
        #https://drive.google.com/drive/folders/1wXcqvpc2EkJ84adcBMkxBeBv8LdIhhYa?usp=drive_link
        drive = authenticate_drive()
        folder_id = "1wXcqvpc2EkJ84adcBMkxBeBv8LdIhhYa"  # あなたのGoogleドライブフォルダIDを入力
        upload_images_to_drive(drive, folder_id, images)
        
        st.write("画像のアップロードが完了しました。")
    else:
        st.write("キーワードを入力してください。")
