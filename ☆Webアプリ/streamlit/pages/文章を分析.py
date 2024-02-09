import streamlit as st
import pandas as pd
from collections import Counter
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlitのテーマ設定
sns.set_theme()

def count_words(text):
    # テキストから単語を抽出してカウント
    words = text.split()
    word_counts = Counter(words)
    return word_counts

def plot_word_frequency(word_counts):
    # 単語の出現回数をグラフ表示
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(word_counts.values()), y=list(word_counts.keys()), palette="viridis")
    plt.title("単語出現回数グラフ")
    plt.xlabel("出現回数")
    plt.ylabel("単語")
    st.pyplot()

def search_word(word_counts, search_term):
    # 特定の単語の出現回数を表示
    st.write(f"単語 '{search_term}' の出現回数: {word_counts.get(search_term, 0)} 回")

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

        # 単語出現回数のグラフ表示
        plot_word_frequency(word_counts)

        # 単語の検索
        search_term = st.text_input("検索する単語を入力してください:")
        if search_term:
            search_word(word_counts, search_term)

if __name__ == "__main__":
    main()
