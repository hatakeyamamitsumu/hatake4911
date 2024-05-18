import streamlit as st
from icrawler.builtin import BingImageCrawler
import os
import shutil
from zipfile import ZipFile
import io

# 画像をクロールして保存
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

# フォルダーを.zipファイルに圧縮してダウンロード
def download_images(images):
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zipf:
        for image_path in images:
            zipf.write(image_path, os.path.basename(image_path))
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

# Streamlitアプリ
st.title("画像クローリングして表示")

keyword = st.text_input("キーワードを入力してください:")
max_images = st.number_input("取得する画像の枚数を入力してください:", min_value=1, max_value=100, value=10)

if st.button("クローリング＆表示"):
    if keyword:
        st.write(f"{keyword} に関連する画像をクローリングしています...")
        images = crawl_images(keyword, max_num=max_images)
        
        if images:
            st.write("取得した画像:")
            for img_path in images:
                st.image(img_path)
            
            if st.button("画像をダウンロード"):
                zip_data = download_images(images)
                st.download_button(label="画像をダウンロード", data=zip_data, file_name="downloaded_images.zip", mime="application/zip")
        else:
            st.write("画像が見つかりませんでした。")
    else:
        st.write("キーワードを入力してください。")
