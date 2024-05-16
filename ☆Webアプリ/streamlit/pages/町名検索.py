import pandas as pd
import streamlit as st

# Google DriveのファイルID
file_id = "1fDInJTb7My6by9Dx70XIByDh8yux-09i"

# ファイルを読み込む
@st.cache
def load_data(file_id):
    url = f"https://drive.google.com/uc?id={file_id}"
    return pd.read_csv(url)

# Streamlitアプリのセットアップ
def main():
    st.title("部分一致検索")

    # CSVファイルを読み込む
    df = load_data(file_id)

    # 都道府県名の入力欄
    prefecture = st.text_input("都道府県名を入力してください：")

    # 市区町村名の入力欄
    city = st.text_input("市区町村名を入力してください：")

    # 大字・丁目名の入力欄
    district = st.text_input("大字・丁目名を入力してください：")

    # 部分一致検索を実行
    if prefecture or city or district:
        filtered_df = df[df["都道府県名"].str.contains(prefecture) &
                         df["市区町村名"].str.contains(city) &
                         df["大字・丁目名"].str.contains(district)]
        st.write(filtered_df)

# Streamlitアプリを実行
if __name__ == "__main__":
    main()
