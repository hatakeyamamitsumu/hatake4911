import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

# Google Sheets 認証情報のファイルパスとスコープ
SP_CREDENTIAL_FILE = st.secrets["aaaa"]

# 認証情報のパスを出力して確認する
st.write(SP_CREDENTIAL_FILE)


