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
def create_zip(image_paths, keyword):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for i, img_path in enumerate(image_paths):
            ext = os.path.splitext(img_path)[1]
            zip_filename = f"{keyword}_{i+1}{ext}"
            zf.write(img_path, zip_filename)
    zip_buffer.seek(0)
    return zip_buffer

# Streamlitアプリ
st.title("画像クローリング・表示")

keyword = st.text_input("キーワードを入力してください（複数入力可能）:")
max_images = st.number_input("取得する画像の枚数を入力してください（上限50）:", min_value=1, max_value=50, value=10)

if st.button("クローリング＆表示"):
    if keyword:
        st.write(f"{keyword} に関連する画像をクローリングしています...")
        images = crawl_images(keyword, max_num=max_images)
        
        if images:
            st.write("取得した画像:")

            # 6列で表示
            columns = st.columns(8)
            for i, img_path in enumerate(images):
                with columns[i % 8]:
                    st.image(img_path, caption=f"Image {i+1}")

            # ZIPファイルのダウンロードボタン
            zip_buffer = create_zip(images, keyword)
            st.download_button(
                label="すべての画像をダウンロード (ZIP)",
                data=zip_buffer,
                file_name=f"{keyword}_images.zip",
                mime="application/zip"
            )
        else:
            st.write("画像が見つかりませんでした。")
    else:
        st.write("キーワードを入力してください。")
