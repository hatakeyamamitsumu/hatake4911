import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

# Streamlitアプリケーションのタイトルを設定

# Google Sheets 認証情報のファイルパスとスコープ
SP_CREDENTIAL_FILE = st.secrets["gcp"]["json_where"]

st.write(SP_CREDENTIAL_FILE)
