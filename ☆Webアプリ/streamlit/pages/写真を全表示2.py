import os
import streamlit as st
from PIL import Image
import base64

def resize_image(image_path, scale_factor=1):
    original_image = Image.open(image_path)
    width, height = original_image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    resized_image = original_image.resize((new_width, new_height))
    return resized_image

def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def main():
    st.title('画像表示とダウンロード')

    # 画像が格納されているフォルダのパス
    folder_path = "/mount/src/hatake4911/☆Webアプリ/画像/東京画像"

    # フォルダ内の画像ファイルの一覧を取得
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if not image_files:
        st.warning("指定されたフォルダ内に画像ファイルが見つかりません。")
        return

    # 画像を5列で表示
    columns = st.columns(5)

    # 選択された画像のパスを保持する変数
    selected_image_path = None

    for i, image_file in enumerate(image_files):
        image_path = os.path.join(folder_path, image_file)
        resized_image = resize_image(image_path)

        with columns[i % 5]:
            # 画像を表示
            st.image(resized_image, caption=image_file, use_column_width=True)

            # 選択された画像をクリックしてダウンロード
            if st.button(f"選択: {image_file}"):
                selected_image_path = image_path

    # 選択された画像があれば、ダウンロードリンクを表示
    if selected_image_path:
        selected_image = Image.open(selected_image_path)
        download_link = get_image_download_link(selected_image, f"selected_image.jpg", 'Download Selected Image')
        st.markdown(download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
