import os
import streamlit as st
import pandas as pd
from PIL import Image

def main():
    st.title("都道府県を塗り分け用CSVファイルと画像の表示")

    # 指定されたフォルダパス
    folder_path = "/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/都道府県を塗り分け用ＣＳＶ/"

    # 指定されたフォルダ内のサブフォルダ一覧を取得
    subfolders = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]

    # サブフォルダが存在するか確認
    if not subfolders:
        st.warning("指定されたフォルダ内にサブフォルダが見つかりません。")
        return

    # サブフォルダの選択
    selected_subfolder = st.selectbox("サブフォルダを選択してください", subfolders)

    # 選択されたサブフォルダ内のすべてのCSVファイル一覧を取得
    csv_files = [file for file in os.listdir(os.path.join(folder_path, selected_subfolder)) if file.endswith('.csv')]

    # CSVファイルが存在するか確認
    if not csv_files:
        st.warning("選択されたサブフォルダ内にCSVファイルが見つかりません。")
        return

    # 選択されたサブフォルダ内のすべての画像ファイル一覧を取得
    image_files = [file for file in os.listdir(os.path.join(folder_path, selected_subfolder))
                   if file.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    # 画像が存在するか確認
    if not image_files:
        st.warning("選択されたサブフォルダ内に画像ファイルが見つかりません。")
        return

    # 画像とCSVファイルを横に並べて表示
    st.subheader("CSVファイルと画像の一覧:")
    for selected_csv, selected_image in zip(csv_files, image_files):
        st.write(f"選択されたCSVファイル: {selected_csv} | 選択された画像: {selected_image}")

        # CSVファイルを表示
        csv_path = os.path.join(folder_path, selected_subfolder, selected_csv)
        df = pd.read_csv(csv_path)
        st.dataframe(df, use_container_width=True)

        # 画像を表示
        image_path = os.path.join(folder_path, selected_subfolder, selected_image)
        image = Image.open(image_path)
        st.image(image, caption=f"{selected_image}", use_column_width=True)

if __name__ == "__main__":
    main()

