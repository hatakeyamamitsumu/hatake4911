import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google ドライブの認証情報
credentials = Credentials.from_service_account_file(
    '/path/to/your/service_account_credentials.json',  # サービスアカウントキーのファイルパスを指定してください
    scopes=['https://www.googleapis.com/auth/drive']
)

# Google ドライブのAPIをビルド
drive_service = build('drive', 'v3', credentials=credentials)

# Googleドライブ内のPythonファイルのID
file_id = 'your_file_id_here'

# Pythonファイルを実行して、変数aの値を取得する関数
def execute_python_script(file_id):
    # Pythonファイルの実行コマンドを構築する
    command = f"python /content/{file_id}.ipynb"  # Google Colabの場合の例です。環境に応じて変更してください。
    # コマンドを実行して、出力を取得する
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout

# Pythonファイルを実行し、変数aの値を取得
a_value = execute_python_script(file_id)

# 変数aの値をStreamlitに表示
st.write("変数aの値:", a_value)
