import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from PIL import Image
import io

from icrawler.builtin import BingImageCrawler
import os
import zipfile






# Google ドライブ API 認証情報
credentials = Credentials.from_service_account_info(
    st.secrets["google"],
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
    columns = st.columns(6)  # 6列で表示する
    for i, image in enumerate(images):
        image_id = image['id']
        file = drive_service.files().get_media(fileId=image_id)
        image_data = io.BytesIO(file.execute())
        img = Image.open(image_data)
        with columns[i % 6]:
            st.image(img, caption=image['name'], use_column_width=True)

# フォルダ内の特定のファイル名を持つ画像を取得する関数
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
    folder_id ='1BIEdWNQ1Iw0nEqf8OpGZXDywXFBiQueN'
    
    st.title('簡易な画像掲示板')

    # ファイル名を検索するための入力欄
    search_query = st.text_input("調べたい画像ファイル名を入力してください（部分一致ＯＫ）：")
    
    if search_query:
        try:
            images = search_images_by_filename(folder_id, search_query)
            if images:
                display_images(images)
            else:
                st.warning('指定された条件に一致する画像が見つかりませんでした。')
        except Exception as e:
            st.error(f'エラーが発生しました: {e}')
    else:
        st.info("検索ワードを入力してください。")

    # 画像をアップロードする
    uploaded_file = st.file_uploader("画像をアップロードしてください（※検索しやすいファイル名を付けておいてください。）", type=['jpg', 'jpeg', 'png'])
    st.write("※アップロードした画像は削除できません。")
    if uploaded_file is not None:
        try:
            upload_image_to_folder(folder_id, uploaded_file)
            st.success("画像が正常にアップロードされました。")
        except Exception as e:
            st.error(f'画像のアップロード中にエラーが発生しました: {e}')

if __name__ == '__main__':
    main()









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
