import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd
import streamlit as st
st.title('簡易な掲示板っぽいアプリ（閲覧コーナー）')
SP_CREDENTIAL_FILE = '/mount/src/hatake4911/☆Webアプリ/秘密鍵/gspread-test-421301-6cd8b0cc0e27.json'

SP_COPE = [
    'https://www.googleapis.com/auth/drive',
    'https://spreadsheets.google.com/feeds'
]
SP_SHEET_KEY = '1GuaN72pbZxQJBsxLTK3n7fAQfLMJIcuUjZ7pBd-R7kc'
SP_SHEET='話題1'
credentials =ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE,SP_COPE)
gc=gspread.authorize(credentials)
sh=gc.open_by_key(SP_SHEET_KEY)
worksheet=sh.worksheet(SP_SHEET)
data=worksheet.get_all_values()
#data

df=pd.DataFrame(data[1:],columns=data[0])
df

#df.sort_values('社員ID')
