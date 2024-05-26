import streamlit as st
import os
import io
import zipfile
from PIL import Image
import time
from icrawler.builtin import BingImageCrawler
from selenium import webdriver
import requests
from bs4 import BeautifulSoup

# 画像をクロールして保存（BingImageCrawlerを使用）
def crawl_images_bing(keyword, max_num=10):
    save_dir = f"./{keyword}_images_bing"
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

# 画像をクロールして保存（Google Imagesを使用）
def fetch_image_urls(query:str, max_links_to_fetch:int, wd):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # wait for more images to load
        # scroll additional times if needed

    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(1)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls

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

if st.button("Bingからクローリング＆表示"):
    if keyword:
        st.write(f"{keyword} に関連する画像をクローリングしています...")
        images_bing = crawl_images_bing(keyword, max_num=max_images)
        
        if images_bing:
            st.write("取得した画像:")

            # 6列で表示
            columns = st.columns(8)
            for i, img_path in enumerate(images_bing):
                with columns[i % 8]:
                    st.image(img_path, caption=f"Bing Image {i+1}")

            # ZIPファイルのダウンロードボタン
            zip_buffer = create_zip(images_bing, keyword)
            st.download_button(
                label="すべての画像をダウンロード (ZIP)",
                data=zip_buffer,
                file_name=f"{keyword}_images_bing.zip",
                mime="application/zip"
            )
        else:
            st.write("画像が見つかりませんでした。")
    else:
        st.write("キーワードを入力してください。")

if st.button("Googleからクローリング＆表示"):
    if keyword:
        st.write(f"{keyword} に関連する画像をクローリングしています...")
        image_urls_google = fetch_image_urls(query=keyword, max_links_to_fetch=max_images, wd=webdriver.Chrome(executable_path="./chromedriver"))
        
        if image_urls_google:
            st.write("取得した画像:")

            # 6列で表示
            columns = st.columns(8)
            for i, img_url in enumerate(image_urls_google):
                response = requests.get(img_url)
                image = Image.open(io.BytesIO(response.content))
                with columns[i % 8]:
                    st.image(image, caption=f"Google Image {i+1}")

            # ZIPファイルのダウンロードボタン
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                for i, img_url in enumerate(image_urls_google):
                    ext = os.path.splitext(img_url)[1]
                    zip_filename = f"{keyword}_google_{i+1}{ext}"
                    img_data = requests.get(img_url).content
                    zf.writestr(zip_filename, img_data)
            zip_buffer.seek(0)

            st.download_button(
                label="すべての画像をダウンロード (ZIP)",
                data=zip_buffer,
                file_name=f"{keyword}_images_google.zip",
                mime="application/zip"
            )
        else:
            st.write("画像が見つかりませんでした
