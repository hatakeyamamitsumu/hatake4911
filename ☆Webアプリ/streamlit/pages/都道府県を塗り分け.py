import os
import streamlit as st
import pandas as pd
from PIL import Image

def main():
    st.title("複数のサブフォルダ内のCSVファイルと画像の表示")
    # 'a' フォルダ内のサブフォルダ一覧を取得　/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/都道府県を塗り分け用ＣＳＶ/博物館の数
    subfolders = [folder for folder in os.listdir('/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/都道府県を塗り分け用ＣＳＶ') if os.path.isdir(os.path.join('/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/都道府県を塗り分け用ＣＳＶ', folder))]

    # サブフォルダが存在するか確認
    if not subfolders:
        st.warning("指定されたフォルダ内にサブフォルダが見つかりません。")
        return

    # サブフォルダの選択
    selected_subfolder = st.selectbox("サブフォルダを選択してください", subfolders)

    # 選択されたサブフォルダ内のCSVファイル一覧を取得
    csv_files = [file for file in os.listdir(os.path.join('a', selected_subfolder)) if file.endswith('.csv')]

    # CSVファイルが存在するか確認
    if not csv_files:
        st.warning("選択されたサブフォルダ内にCSVファイルが見つかりません。")
        return

    # CSVファイルの選択
    selected_csv = st.selectbox("CSVファイルを選択してください", csv_files)

    # 選択されたCSVファイルを表示
    st.subheader(f"選択されたCSVファイル: {selected_csv}")
    csv_path = os.path.join('a', selected_subfolder, selected_csv)
    df = pd.read_csv(csv_path)
    st.dataframe(df)

    # 選択されたサブフォルダ内の画像ファイル一覧を取得
    image_files = [file for file in os.listdir(os.path.join('a', selected_subfolder))
                   if file.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    # 画像が存在するか確認
    if not image_files:
        st.warning("選択されたサブフォルダ内に画像ファイルが見つかりません。")
        return

    # 画像の選択
    selected_image = st.selectbox("画像を選択してください", image_files)

    # 選択された画像を表示
    st.subheader(f"選択された画像: {selected_image}")
    image_path = os.path.join('a', selected_subfolder, selected_image)
    image = Image.open(image_path)
    st.image(image, caption=f"{selected_image}", use_column_width=True)

if __name__ == "__main__":
    main()
