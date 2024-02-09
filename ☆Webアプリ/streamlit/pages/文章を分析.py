import streamlit as st
import pandas as pd
from collections import Counter
from io import StringIO

def count_words(text):
    # テキストから単語を抽出してカウント
    words = text.split()
    word_counts = Counter(words)
    return word_counts

def search_word_count(text, search_term):
    # テキスト中で検索した単語の出現回数を数える
    words = text.split()
    search_count = Counter(words)[search_term]
    return search_count

def main():
    st.title("単語出現回数カウンター")

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

        # 単語の検索
        search_term = st.text_input("検索する単語を入力してください:")
        if search_term:
            search_count = search_word_count(text, search_term)
            st.write(f"単語 '{search_term}' の出現回数: {search_count} 回")

if __name__ == "__main__":
    main()
