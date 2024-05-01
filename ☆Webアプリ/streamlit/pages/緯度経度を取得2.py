import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Googleドライブの認証情報
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'path/to/your/credentials.json',  # 認証情報ファイルのパスを指定してください
    ['https://www.googleapis.com/auth/drive']
)

# Googleドライブに接続
gc = gspread.authorize(credentials)

# Googleドライブ内のCSVファイルのパス
file_path = '/path/to/your/csv/file.csv'  # CSVファイルのパスを指定してください

# ユーザーからの緯度と経度の入力を受け取る
latitude = st.number_input("緯度を入力してください", value=35.6895, step=0.0001)
longitude = st.number_input("経度を入力してください", value=139.6917, step=0.0001)

# 入力された緯度経度をDataFrameに追加
new_data = {'Latitude': [latitude], 'Longitude': [longitude]}
new_df = pd.DataFrame(new_data)

# DataFrameをGoogleドライブのCSVファイルに書き込む
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1GOR9sw1Nkon2qxMOfIDiq0zF4TICipRV')  # GoogleスプレッドシートのURLを指定してください
worksheet = sh.get_worksheet(0)  # ワークシートのインデックスを指定してください

# データを追加する行の位置を取得
next_row = len(worksheet.get_all_values()) + 1

# データを書き込む
worksheet.insert_row(new_df.values[0].tolist(), next_row)

# 結果を表示
st.success("緯度経度がCSVファイルに書き込まれました。")
