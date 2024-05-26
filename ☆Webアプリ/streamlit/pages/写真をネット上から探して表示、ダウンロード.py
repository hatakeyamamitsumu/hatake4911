import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# Google Imagesから画像URLを取得する関数
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

# Streamlitアプリ
st.title("画像クローリング・表示")

keyword = st.text_input("キーワードを入力してください（複数入力可能）:")
max_images = st.number_input("取得する画像の枚数を入力してください（上限50）:", min_value=1, max_value=50, value=10)

if st.button("クローリング＆表示"):
    if keyword:
        st.write(f"{keyword} に関連する画像をクローリングしています...")
        image_urls = fetch_image_urls(query=keyword, max_links_to_fetch=max_images, wd=webdriver.Chrome(executable_path="./chromedriver"))
        
        if image_urls:
            st.write("取得した画像:")

            # 6列で表示
            columns = st.columns(8)
            for i, img_url in enumerate(image_urls):
                with columns[i % 8]:
                    response = requests.get(img_url)
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, caption=f"Image {i+1}")

            # ZIPファイルのダウンロードボタン
            zip_buffer = create_zip(image_urls, keyword)
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

