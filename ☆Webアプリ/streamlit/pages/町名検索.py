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

    # 部分一致検索の条件入力
    search_query = st.text_input("検索クエリを入力してください：")

    # 部分一致検索を実行
    if search_query:
        filtered_df = df[df["都道府県名"].str.contains(search_query) |
                         df["市区町村名"].str.contains(search_query) |
                         df["大字・丁目名"].str.contains(search_query)]
        st.write(filtered_df)

# Streamlitアプリを実行
if __name__ == "__main__":
    main()
