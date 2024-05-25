import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st

# Streamlitアプリケーションのタイトルを設定
st.title('簡易な掲示板')

# Google Sheets 認証情報とスコープをsecretsから取得
SP_SCOPE = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']

# 認証情報の読み込みと認証
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], SP_SCOPE)
gc = gspread.authorize(credentials)

# スプレッドシートの指定
#SP_SHEET_KEY = '1GuaN72pbZxQJBsxLTK3n7fAQfLMJIcuUjZ7pBd-R7kc'
SP_SHEET_KEY = st.secrets["spreadsheet"]["spreadsheet_key"]

sh = gc.open_by_key(SP_SHEET_KEY)

# スプレッドシート内のシート名を取得
sheet_names = [worksheet.title for worksheet in sh.worksheets()]

# ユーザーが選択するモードを決定するためのセレクトボックスを追加
selected_mode = st.radio("選択してください:", ("閲覧", "書き込み"))

if selected_mode == "閲覧":
    # シートの選択
    selected_sheet_name = st.selectbox("操作したいシートを選択してください", sheet_names)
    worksheet = sh.worksheet(selected_sheet_name)
    
    # データ取得
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    # データフレームを表示
    st.write(df)

elif selected_mode == "書き込み":
    # シートの選択
    selected_sheet_name = st.selectbox("書き込むシートを選択してください", sheet_names)
    worksheet = sh.worksheet(selected_sheet_name)

    # 現在のデータ取得
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    # ユーザーから新しいデータの入力を受け取る
    new_data = []
    for i, column in enumerate(df.columns):
        new_value = st.text_input("{}を入力してください: ".format(column), key=str(i))
        new_data.append(new_value)

    # 新しいデータを追加
    updated_df = df.append(pd.Series(new_data, index=df.columns), ignore_index=True)

    # 書き込みボタンが押されたらスプレッドシートに書き込む
    if st.button('メッセージを書き込む（書き込んだら消せません）'):
        # 新しいデータをスプレッドシートに書き込む
        worksheet.update([updated_df.columns.values.tolist()] + updated_df.values.tolist())
        st.success("新しいメッセージを書き込みました。")
