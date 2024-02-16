
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
    st.title("Image Viewer")

    folder_path = "/mount/src/hatake4911/☆Webアプリ/画像"  # ご自身のフォルダのパスに変更してください
    st.sidebar.header("Search Settings")
    keyword = st.sidebar.text_input("Enter keyword to filter images")

    if st.button("Search"):
        if keyword:
            matching_images = filter_images(folder_path, keyword)
            if matching_images:
                display_matching_images(folder_path, matching_images)
            else:
                st.warning("No matching images found.")
        else:
            st.warning("Please enter a keyword to search.")

if __name__ == "__main__":
    main()
