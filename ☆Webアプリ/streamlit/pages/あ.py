import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

# Streamlitアプリケーションのタイトルを設定
st.title('簡易な掲示板')

# Google Sheets 認証情報のファイルパスとスコープ
SP_CREDENTIAL_FILE = st.secrets["gcp"]["json_where"]
SP_SHEET_KEY = st.secrets["gcp"]["sp_sheet_key"]
SP_SCOPE = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']

st.write(SP_CREDENTIAL_FILE)
