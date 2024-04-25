import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

# Streamlitアプリケーションのタイトルを設定
st.title('簡易な掲示板っぽいアプリ')

# Google Sheets 認証情報のファイルパスとスコープ
SP_CREDENTIAL_FILE = '/mount/src/hatake4911/☆Webアプリ/秘密鍵/gspread-test-421301-6cd8b0cc0e27.json'
SP_SCOPE = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
SP_SHEET_KEY = '1GuaN72pbZxQJBsxLTK3n7fAQfLMJIcuUjZ7pBd-R7kc'

# 認証情報の読み込みと認証
credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
gc = gspread.authorize(credentials)

# スプレッドシートの選択
selected_sheet = st.selectbox("シートを選択してください:", gc.open_by_key(SP_SHEET_KEY).worksheet_titles())

# 選択されたシートのデータ取得
worksheet = gc.open_by_key(SP_SHEET_KEY).worksheet(selected_sheet)
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

# ユーザーから新しいデータの入力を受け取る
new_data = []
for i, column in enumerate(df.columns):
    new_value = st.text_input("新しい{}を入力してください: ".format(column), key=str(i))
    new_data.append(new_value)

# 新しいデータを追加
updated_df = df.append(pd.Series(new_data, index=df.columns), ignore_index=True)

# 書き込みボタンが押されたらスプレッドシートに書き込む
if st.button('データをスプレッドシートに書き込む'):
    # 新しいデータをスプレッドシートに書き込む
    worksheet.update([updated_df.columns.values.tolist()] + updated_df.values.tolist())
    st.success("新しいデータをスプレッドシートに書き込みました。")

