import os
import streamlit as st
from PIL import Image

def resize_image(image_path, scale_factor=0.1):
    original_image = Image.open(image_path)
    width, height = original_image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    resized_image = original_image.resize((new_width, new_height))
    return resized_image

def main():
    st.title('画像表示')

    # 画像が格納されているフォルダのパス
    folder_path = "/mount/src/hatake4911/☆Webアプリ/画像/東京画像"

    # フォルダ内の画像ファイルの一覧を取得
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if not image_files:
        st.warning("指定されたフォルダ内に画像ファイルが見つかりません。")
        return

    # 画像を1/10サイズにして3列で表示
    container1, container2, container3 = st.beta_columns(3)

    for i, image_file in enumerate(image_files):
        image_path = os.path.join(folder_path, image_file)
        resized_image = resize_image(image_path)

        if i % 3 == 0:
            with container1:
                st.image(resized_image, caption=image_file, use_column_width=True)
        elif i % 3 == 1:
            with container2:
                st.image(resized_image, caption=image_file, use_column_width=True)
        else:
            with container3:
                st.image(resized_image, caption=image_file, use_column_width=True)

if __name__ == "__main__":
    main()
