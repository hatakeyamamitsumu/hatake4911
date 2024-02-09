import streamlit as st
import pandas as pd
from io import StringIO

def count_words(text):
    # テキストから単語を抽出してカウント
    words = text.split()
    word_counts = Counter(words)
    return word_counts

def filter_and_download(text, filter_words):
    # 複数の単語が含まれる行をフィルタリング
    lines_with_words = [line for line in text.split('\n') if any(word.lower() in line.lower() for word in filter_words)]

    if lines_with_words:
        # 結果をデータフレームに変換
        result_df = pd.DataFrame({"行": lines_with_words})

        # 結果を表示
        st.write(f"### '{', '.join(filter_words)}' を含む行のリスト")
        st.dataframe(result_df)

        # 結果をCSVファイルとしてダウンロード
        csv_data = StringIO()
        result_df.to_csv(csv_data, index=False)
        st.download_button(label="CSVファイルとしてダウンロード", data=csv_data.getvalue(), file_name="filtered_data.csv", key="download_button")
    else:
        st.write(f"テキストに '{', '.join(filter_words)}' を含む行は見つかりませんでした。")

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
        st.write("### 単語出現回数リスト")
        st.dataframe(result_df)

        # フィルタリングする単語を入力
        filter_words = st.text_input("フィルタリングする単語をスペースで区切って入力してください:")

        if filter_words:
            filter_words = filter_words.split()
            filter_and_download(text, filter_words)

if __name__ == "__main__":
    main()
