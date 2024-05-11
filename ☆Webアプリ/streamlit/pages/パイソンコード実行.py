import streamlit as st
import subprocess
import re

# Streamlitアプリのタイトル　
st.title("Googleドライブ内のPythonファイルの実行")

# Googleドライブ内のPythonファイルのURL　https://colab.research.google.com/drive/1ABCFiAKYI6buI2k-htVLABm3kDKhFRWE?usp=drive_link
google_drive_url = "https://colab.research.google.com/drive/1ABCFiAKYI6buI2k-htVLABm3kDKhFRWE?usp=drive_link"

# ファイルIDを抽出する関数
def extract_file_id_from_url(url):
    pattern = r'/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

# ファイルIDを抽出
file_id = extract_file_id_from_url(google_drive_url)

# Googleドライブ内のPythonファイルのパス
google_drive_path = f"/content/{file_id}.py"  # Google Colabの場合の例です。環境に応じて変更してください。

# Googleドライブ内のPythonファイルを実行して、出力を取得する関数
def execute_python_script(script_path):
    # コマンドを構築する
    command = ["python", script_path]
    # コマンドを実行して、出力を取得する
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

# Googleドライブ内のPythonファイルを実行し、出力を取得
output = execute_python_script(google_drive_path)

# 出力をStreamlitに表示
st.code(output)
