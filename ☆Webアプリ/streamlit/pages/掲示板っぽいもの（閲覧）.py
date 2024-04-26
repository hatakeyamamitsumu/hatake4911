import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd
import streamlit as st

# Streamlitアプリケーションのタイトルを設定
st.title('簡易な掲示板っぽいアプリ（閲覧コーナー）')

# Google Sheets 認証情報のファイルパスとスコープ
SP_CREDENTIAL_FILE = '/mount/src/hatake4911/☆Webアプリ/秘密鍵/gspread-test-421301-6cd8b0cc0e27.json'
SP_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://spreadsheets.google.com/feeds'
]
SP_SHEET_KEY = '1GuaN72pbZxQJBsxLTK3n7fAQfLMJIcuUjZ7pBd-R7kc'

# 認証情報の読み込みと認証
credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
gc = gspread.authorize(credentials)

# スプレッドシートの指定
sh = gc.open_by_key(SP_SHEET_KEY)

# スプレッドシート内のシート名を取得
sheet_names = [worksheet.title for worksheet in sh.worksheets()]

# セレクトボックスでシートを選択
selected_sheet_name = st.selectbox("スプレッドシートのシート名を選択してください", sheet_names)

# 選択したシートを開く
worksheet = sh.worksheet(selected_sheet_name)

# データ取得
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

# データフレームを表示
df

#df.sort_values('社員ID')
