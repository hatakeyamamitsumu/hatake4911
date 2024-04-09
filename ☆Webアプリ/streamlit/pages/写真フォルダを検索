import os
import streamlit as st
from PIL import Image

def filter_images(folder_path, keyword1, keyword2, keyword3):
    matching_images = []
    for filename in os.listdir(folder_path):
        if (
            keyword1.lower() in filename.lower() and 
            keyword2.lower() in filename.lower() and 
            keyword3.lower() in filename.lower() and 
            filename.lower().endswith(('.png', '.jpg', '.jpeg'))
        ):
            matching_images.append(filename)
    return matching_images

def display_matching_images(folder_path, matching_images):
    for filename in matching_images:
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)
        st.image(image, caption=filename)

def main():
    st.title("写真を検索")
    st.write("Hatが保管してある写真用フォルダの中の写真をファイル名で検索し、絞り込んで表示します。")

    base_folder_path = "/mount/src/hatake4911/☆Webアプリ/画像"
    subfolders = [f for f in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, f))]
    selected_subfolder = st.sidebar.selectbox("検索対象のフォルダを選択してください", subfolders, index=0)
    
    folder_path = os.path.join(base_folder_path, selected_subfolder)
    keyword1 = st.sidebar.text_input("検索条件1を入力してください")
    keyword2 = st.sidebar.text_input("検索条件2を入力してください")
    keyword3 = st.sidebar.text_input("検索条件3を入力してください")

    if st.button("検索開始"):
        if any((keyword1, keyword2, keyword3)):
            matching_images = filter_images(folder_path, keyword1, keyword2, keyword3)
            if matching_images:
                display_matching_images(folder_path, matching_images)
            else:
                st.warning("一致する写真が見つかりませんでした。")
        else:
            st.warning("検索条件を入力してください。")

if __name__ == "__main__":
    main()
