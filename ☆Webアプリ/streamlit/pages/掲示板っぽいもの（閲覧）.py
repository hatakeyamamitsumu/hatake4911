import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd
import streamlit as st

# Google Sheetsの認証情報ファイルパス
SP_CREDENTIAL_FILE = '/mount/src/hatake4911/☆Webアプリ/秘密鍵/gspread-test-421301-6cd8b0cc0e27.json'

# Google Sheets APIのスコープ
SP_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://spreadsheets.google.com/feeds'
]

# Google Sheetsのキー
SP_SHEET_KEY = '1GuaN72pbZxQJBsxLTK3n7fAQfLMJIcuUjZ7pBd-R7kc'

# Google Sheetsからシート名を取得する関数
def get_sheet_names(credentials, sheet_key):
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(sheet_key)
    return [worksheet.title for worksheet in sh.worksheets()]

# Streamlitアプリの構築
def main():
    # サイドバーにタイトルを表示
    st.sidebar.title("Google Sheets データ閲覧")

    # サイドバーに情報を表示
    st.sidebar.info("このアプリでは、Google Sheetsからデータを読み込んで閲覧します。")

    # シート名を取得
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
    sheet_names = get_sheet_names(credentials, SP_SHEET_KEY)

    # セレクトボックスでシート名を選択
    selected_sheet = st.sidebar.selectbox("シートを選択してください:", sheet_names)

    # 選択されたシートのデータを取得して表示
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SP_SHEET_KEY)
    worksheet = sh.worksheet(selected_sheet)
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    # データを表示
    st.write(f"選択されたシート: {selected_sheet}")
    st.write(df)

if __name__ == "__main__":
    main()
