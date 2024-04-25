import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd
import streamlit as st

SP_CREDENTIAL_FILE = '/mount/src/hatake4911/☆Webアプリ/秘密鍵/gspread-test-421301-6cd8b0cc0e27.json'

SP_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://spreadsheets.google.com/feeds'
]
SP_SHEET_KEY = '1GuaN72pbZxQJBsxLTK3n7fAQfLMJIcuUjZ7pBd-R7kc'

# Google Sheetsからシート名を取得する関数
def get_sheet_names(credentials, sheet_key):
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(sheet_key)
    return [worksheet.title for worksheet in sh.worksheets()]

# シート名の取得
credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
sheet_names = get_sheet_names(credentials, SP_SHEET_KEY)

# セレクトボックスでシート名を選択
selected_sheet = st.selectbox("シートを選択してください:", sheet_names)

# 選択されたシート名を表示
st.write("選択されたシート:", selected_sheet)
