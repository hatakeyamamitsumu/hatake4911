import streamlit as st
from icrawler.builtin import BingImageCrawler
import os
import zipfile
import io
from PIL import Image

# 画像をクロールして保存
def crawl_images(keyword, max_num=10):
    save_dir = f"./{keyword}_images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # BingImageCrawlerのmax_num引数はcrawlメソッドに渡す
    crawler = BingImageCrawler(storage={"root_dir": save_dir})
    crawler.crawl(keyword=keyword, max_num=max_num)
    
    # ダウンロードした画像のパスを取得
    image_paths = []
    for root, dirs, files in os.walk(save_dir):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png')):
                image_paths.append(os.path.join(root, file))
    return image_paths

# 画像をZIPファイルに圧縮
def create_zip(image_paths):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for img_path in image_paths:
            zf.write(img_path, os.path.basename(img_path))
    zip_buffer.seek(0)
    return zip_buffer

# Streamlitアプリ
st.title("画像クローリング・表示")

keyword_input = st.text_input("キーワードを入力してください（複数入力可能）:")
max_images = st.number_input("取得する画像の枚数を入力してください（上限20）:", min_value=1, max_value=20, value=10)

if st.button("クローリング＆表示"):
    if keyword_input:
        keywords = [keyword.strip() for keyword in keyword_input.split(",")]
        all_images = []
        for keyword in keywords:
            st.write(f"{keyword} に関連する画像をクローリングしています...")
            images = crawl_images(keyword, max_num=max_images)
            if images:
                st.write(f"取得した画像 ({keyword}):")
                for img_path in images:
                    image = Image.open(img_path)
                    st.image(image)
                    st.write(f"ファイル名: {os.path.basename(img_path)}")
                    st.write(f"サイズ: {image.size}")
                    all_images.append(img_path)
            else:
                st.write(f"{keyword} に関連する画像が見つかりませんでした。")
        
        if all_images:
            selected_images = st.multiselect("ダウンロードする画像を選択してください", all_images, format_func=lambda x: os.path.basename(x))
            if selected_images:
                zip_buffer = create_zip(selected_images)
                st.download_button(
                    label="選択した画像をダウンロード (ZIP)",
                    data=zip_buffer,
                    file_name=f"selected_images.zip",
                    mime="application/zip"
                )
            else:
                st.write("画像が選択されていません。")
        else:
            st.write("いずれのキーワードに関連する画像も見つかりませんでした。")
    else:
        st.write("キーワードを入力してください。")
