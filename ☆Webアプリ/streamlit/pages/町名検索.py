import pandas as pd
import streamlit as st

# GoogleドライブからCSVファイルを読み込む。
@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

# Streamlitアプリのセットアップ
def main():
    st.title("部分一致検索")

    # Googleドライブ内のCSVファイルパス
    file_path = "/content/drive/MyDrive/a.csv"

    # CSVファイルを読み込む
    df = load_data(file_path)

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
