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
  uploaded_file = st.file_uploader("テキストファイルまたはワードファイルをアップロードしてください", type=["txt", "docx"])

  if uploaded_file is not None:
    # Read the uploaded file
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
      text = read_word_file(uploaded_file)
    else:
      text = uploaded_file.read().decode("utf-8")

    # Add newlines
    text = add_newlines(text)

    # Display results
    st.write("### 抽出結果")
    st.write(text)

if __name__ == "__main__":
  main()
