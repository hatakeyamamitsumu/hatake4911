import streamlit as st
import subprocess
import requests

# Streamlitアプリのタイトル
st.title("Googleドライブ内のPythonファイルの実行")

# Googleドライブ内の.ipynbファイルの共有リンク
google_drive_url = "https://colab.research.google.com/drive/19Rm3z4QAolOk0HoBcp7AOR9bR8YjwSTW?usp=sharing"

# Google Colabで.ipynbファイルを実行して実行結果を取得する関数
def execute_ipynb_file(ipynb_url):
    # Google Colabの実行URLを構築する
    colab_url = f"https://colab.research.google.com/drive/{ipynb_url}"
    # Google ColabのAPIを使用して.ipynbファイルを実行する
    response = requests.get(colab_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Googleドライブ内の.ipynbファイルを実行し、実行結果を取得
execution_result = execute_ipynb_file(google_drive_url)

# 実行結果をStreamlitに表示
if execution_result is not None:
    st.code(execution_result)
else:
    st.error("ファイルの実行に失敗しました。")
