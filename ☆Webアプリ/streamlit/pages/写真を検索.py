import os
import streamlit as st
from PIL import Image

def filter_images(folder_path, keyword):
    matching_images = []
    for filename in os.listdir(folder_path):
        if keyword.lower() in filename.lower() and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            matching_images.append(filename)
    return matching_images

def display_matching_images(folder_path, matching_images):
    for filename in matching_images:
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)
        st.image(image, caption=filename)

def main():
    st.title("写真を検索")
    st.text("左側のウィンドウから入力してください")

    base_folder_path = "/mount/src/hatake4911/☆Webアプリ/画像"
    subfolders = [f for f in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, f))]
    selected_subfolder = st.sidebar.selectbox("検索対象のサブフォルダを選択してください", subfolders, index=0)
    
    folder_path = os.path.join(base_folder_path, selected_subfolder)
    keyword = st.sidebar.text_input("検索する単語を入力してください")

    if st.button("検索開始"):
        if keyword:
            matching_images = filter_images(folder_path, keyword)
            if matching_images:
                display_matching_images(folder_path, matching_images)
            else:
                st.warning("一致する写真が見つかりませんでした。")
        else:
            st.warning("検索する単語を入力してください。")

if __name__ == "__main__":
    main()
