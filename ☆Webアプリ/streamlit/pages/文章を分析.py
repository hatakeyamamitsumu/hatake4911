import streamlit as st
import pandas as pd
from collections import Counter
from io import StringIO

def count_words(text):
    # テキストから単語を抽出してカウント
    words = text.split()
    word_counts = Counter(words)
    return word_counts

def filter_and_download(text, filter_word):
    # 特定の単語が含まれる行をフィルタリング
    lines_with_word = [line for line in text.split('\n') if filter_word.lower() in line.lower()]

    if lines_with_word:
        # 結果をデータフレームに変換
        result_df = pd.DataFrame({"行": lines_with_word})

        # 結果を表示
        st.write(f"### '{filter_word}' を含む行のリスト")
        st.dataframe(result_df)

        # 結果をCSVファイルとしてダウンロード
        csv_data = StringIO()
        result_df.to_csv(csv_data, index=False)
        st.download_button(label="CSVファイルとしてダウンロード", data=csv_data.getvalue(), file_name="filtered_data.csv", key="download_button")
    else:
        st.write(f"テキストに '{filter_word}' を含む行は見つかりませんでした。")

def main():
    st.title("文章フィルター")

    # ファイルアップロード
    uploaded_file = st.file_uploader("テキストファイルをアップロードしてください", type=["txt"])

    if uploaded_file is not None:
        # アップロードされたファイルを読み込む
        text = uploaded_file.read().decode("utf-8")

        # 単語出現回数をカウント
        word_counts = count_words(text)

        # 結果をデータフレームに変換
        result_df = pd.DataFrame(list(word_counts.items()), columns=['単語', '出現回数'])

        # 結果を表示
        st.write("### 原本")
        st.dataframe(result_df)

        # フィルタリングする単語を入力
        filter_word = st.text_input("フィルタリングする単語を入力してください:")
        if filter_word:
            filter_and_download(text, filter_word)

if __name__ == "__main__":
    main()
