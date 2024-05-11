import streamlit as st
import subprocess
import re
from google.colab import drive

# Streamlitアプリのタイトル
st.title("Googleドライブ内のPythonファイルの実行")

# Googleドライブ内のPythonファイルのURL
google_drive_url = "https://colab.research.google.com/drive/19Rm3z4QAolOk0HoBcp7AOR9bR8YjwSTW?usp=sharing"

# ファイルIDを抽出する関数
def extract_file_id_from_url(url):
    pattern = r'/drive/([a-zA-Z0-9_-]+)\?'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

# Googleドライブ内のPythonファイルのパス
file_id = extract_file_id_from_url(google_drive_url)
drive.mount('/content/drive')
google_drive_path = f"/content/drive/MyDrive/{file_id}.ipynb" 

# Google Colabノートブックの実行
subprocess.run(["jupyter", "nbconvert", "--to", "python", google_drive_path])

# 出力ファイルのパス
output_file_path = "/content/drive/MyDrive/output.txt"

# 出力ファイルの内容を読み込んで表示
with open(output_file_path, "r") as file:
    output_content = file.read()

# 出力をStreamlitに表示
st.code(output_content)
