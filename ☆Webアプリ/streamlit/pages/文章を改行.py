import streamlit as st
import pandas as pd
from io import StringIO
from docx import Document

def add_newlines(text):
  # Add newlines after periods, dots, and semicolons
  text = text.replace(".", ".\n").replace(". ", ".\n").replace("．", "．\n").replace("． ", "．\n").replace("」", "」\n")
  # Add newlines before quotation marks
  text = text.replace("「", "\n「")
  return text

def main():
  st.title("テキストファイルから文章を抽出")
  st.write("テキストファイルをアップロードし、句読点の後で改行、そして「の前で改行するアプリです。")

  # File upload
  uploaded_file_utf8 = st.file_uploader("UTF-8テキストファイルまたはワードファイルをアップロードしてください", type=["txt", "docx"], encoding="utf-8")
  uploaded_file_shift_jis = st.file_uploader("Shift-JISテキストファイルまたはワードファイルをアップロードしてください", type=["txt", "docx"], encoding="shift-jis")

  if uploaded_file_utf8 is not None:
    # Read the uploaded file
    if uploaded_file_utf8.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
      text = read_word_file(uploaded_file_utf8)
    else:
      text = uploaded_file_utf8.read().decode("utf-8")

    # Add newlines
    text = add_newlines(text)

    # Display results
    st.write("### UTF-8 抽出結果")
    st.write(text)

  if uploaded_file_shift_jis is not None:
    # Read the uploaded file
    if uploaded_file_shift_jis.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
      text = read_word_file(uploaded_file_shift_jis)
    else:
      text = uploaded_file_shift_jis.read().decode("shift-jis")

    # Add newlines
    text = add_newlines(text)

    # Display results
    st.write("### Shift-JIS 抽出結果")
    st.write(text)

if __name__ == "__main__":
  main()
