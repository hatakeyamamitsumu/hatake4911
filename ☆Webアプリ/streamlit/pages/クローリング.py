import streamlit as st
import requests
from bs4 import BeautifulSoup
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Google Drive認証
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

# 画像をクローリングしてダウンロード
def crawl_images(keyword):
    url = f"https://www.google.com/search?tbm=isch&q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")

    image_urls = [img["src"] for img in images[:10]]  # 最初の10枚の画像URLを取得
    downloaded_images = []

    for i, img_url in enumerate(image_urls):
        img_data = requests.get(img_url).content
        img_path = f"image_{i}.jpg"
        with open(img_path, "wb") as img_file:
            img_file.write(img_data)
        downloaded_images.append(img_path)

    return downloaded_images

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

if st.button("クローリング＆アップロード"):
    if keyword:
        st.write(f"{keyword} に関連する画像をクローリングしています...")
        images = crawl_images(keyword)
        st.write("画像をGoogleドライブにアップロードしています...")
        
        drive = authenticate_drive()
        folder_id = "1wXcqvpc2EkJ84adcBMkxBeBv8LdIhhYa"  # あなたのGoogleドライブフォルダIDを入力
        upload_images_to_drive(drive, folder_id, images)
        
        st.write("画像のアップロードが完了しました。")
    else:
        st.write("キーワードを入力してください。")
