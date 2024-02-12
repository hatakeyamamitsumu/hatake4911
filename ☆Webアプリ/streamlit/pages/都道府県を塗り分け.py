import os
import streamlit as st
import pandas as pd
from PIL import Image

def main():
    st.title("都道府県を塗り分け用CSVファイルと対応する画像の表示")

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

    # すべてのCSVファイルを表示
    st.subheader("CSVファイルと画像の対応表示:")
    for selected_csv in csv_files:
        st.write(f"選択されたCSVファイル: {selected_csv}")

        # CSVファイルを表示
        csv_path = os.path.join(folder_path, selected_subfolder, selected_csv)
        df = pd.read_csv(csv_path)
        st.dataframe(df, use_container_width=True)

        # 選択されたCSVファイルに対応する画像一覧を取得
        image_files = [file for file in os.listdir(os.path.join(folder_path, selected_subfolder))
                       if file.startswith(selected_csv.split('.')[0]) and file.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        # 画像が存在するか確認
        if not image_files:
            st.warning(f"{selected_csv}に対応する画像ファイルが見つかりません。")
            continue

        # すべての画像を横に表示
        images = [Image.open(os.path.join(folder_path, selected_subfolder, selected_image)) for selected_image in image_files]
        st.image(images, caption=image_files, use_column_width=True)

if __name__ == "__main__":
    main()
