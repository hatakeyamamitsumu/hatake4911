import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

# Streamlitアプリケーションのタイトルを設定
st.title('簡易な掲示板っぽいアプリ')

# Google Sheets 認証情報のファイルパスとスコープ
SP_CREDENTIAL_FILE = '/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json'
SP_SCOPE = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
SP_SHEET_KEY = '1GuaN72pbZxQJBsxLTK3n7fAQfLMJIcuUjZ7pBd-R7kc'

# 認証情報の読み込みと認証
credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_SCOPE)
gc = gspread.authorize(credentials)

# スプレッドシートの指定
sh = gc.open_by_key(SP_SHEET_KEY)

# スプレッドシート内のシート名を取得
sheet_names = [worksheet.title for worksheet in sh.worksheets()]

# 書き込み機能
if '書き込み' in st.session_state:
    # 選択したシートを開く
    worksheet = sh.worksheet(st.session_state.selected_sheet_name)
    
    # 新しいデータをユーザーから受け取る
    new_data = []
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    for i, column in enumerate(df.columns):
        new_value = st.text_input("{}を入力してください: ".format(column), key=str(i))
        new_data.append(new_value)

    # 新しいデータを追加
    updated_df = df.append(pd.Series(new_data, index=df.columns), ignore_index=True)

    # 新しいデータをスプレッドシートに書き込む
    worksheet.update([updated_df.columns.values.tolist()] + updated_df.values.tolist())
    st.success("新しいメッセージを書き込みました。")
else:
    # 読み込み機能
    # セレクトボックスでシートを選択
    # セレクトボックスでシートを選択
    selected_sheet_name = st.selectbox("読みたいテーマを選択してください", sheet_names, key='selected_sheet_name')
    st.session_state.selected_sheet_name = selected_sheet_name


    # 選択したシートを開く
    worksheet = sh.worksheet(selected_sheet_name)

    # データ取得
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    # データフレームを表示
    df

# メッセージを書き込むボタン
if '書き込む' not in st.session_state:
    st.session_state.書き込む = st.button('メッセージを書き込む（書き込んだら消せません）')
