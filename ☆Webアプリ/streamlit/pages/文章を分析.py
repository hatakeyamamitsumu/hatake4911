import streamlit as st
import pandas as pd
from io import StringIO

def filter_and_display(text, filter_word):
    # 特定の単語が含まれる行をフィルタリング
    lines_with_word = [line for line in text.split('\n') if filter_word.lower() in line.lower()]

    if lines_with_word:
        # 結果を表示
        st.write(f"### '{filter_word}' を含む行のリスト")
        st.text("\n".join(lines_with_word))
    else:
        st.write(f"テキストに '{filter_word}' を含む行は見つかりませんでした。")

def main():
    st.title("テキスト行フィルター")

    # テキストファイルアップロード
    uploaded_file = st.file_uploader("テキストファイルをアップロードしてください", type=["txt"])

    if uploaded_file is not None:
        # アップロードされたファイルを読み込む
        text = uploaded_file.read().decode("utf-8")

        # フィルタリングする単語を入力
        filter_word = st.text_input("フィルタリングする単語を入力してください:")
        if filter_word:
            filter_and_display(text, filter_word)

if __name__ == "__main__":
    main()

