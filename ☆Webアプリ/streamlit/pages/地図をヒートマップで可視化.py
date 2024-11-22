import streamlit as st
import pandas as pd
import requests
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# Streamlitアプリのヘッダー
st.header("グーグルドライブ内のCSVデータをもとにヒートマップを表示")
st.text('主に国土地理院データより引用。')

# Google Drive APIの認証情報
scope = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_info(st.secrets["google"], scopes=scope)
service = build('drive', 'v3', credentials=creds)

# Google DriveフォルダーID
drive_folder_id = "1f3XeJDSoEydQHkw867Mt26NUGe2MPJJ1"

# 指定したGoogle Driveフォルダー内のファイルをリストアップする関数
def list_drive_files(folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query).execute()
    files = results.get('files', [])
    return files

# 選択されたフォルダー内のファイルを取得
folders = list_drive_files(drive_folder_id)
folder_names = [folder['name'] for folder in folders]
folder_ids = {folder['name']: folder['id'] for folder in folders}
selected_folder_name = st.selectbox("フォルダを選択してください", folder_names)
selected_folder_id = folder_ids[selected_folder_name]

# 選択されたフォルダー内のCSVファイルを取得
csv_files = list_drive_files(selected_folder_id)
csv_file_names = [file['name'] for file in csv_files if file['name'].endswith('.csv')]
csv_file_ids = {file['name']: file['id'] for file in csv_files if file['name'].endswith('.csv')}
selected_file_name = st.selectbox("CSVファイルを選択してください", csv_file_names)
selected_file_id = csv_file_ids[selected_file_name]

# 選択されたCSVファイルをダウンロードする
file_url = f"https://drive.google.com/uc?id={selected_file_id}"
csv_file_path = f"/tmp/{selected_file_name}"
response = requests.get(file_url)
with open(csv_file_path, 'wb') as f:
    f.write(response.content)

# ダウンロードしたCSVファイルからデータを読み込む
data = pd.read_csv(csv_file_path)

# データに緯度、経度、標高の列が含まれているかチェック
latitude_column = data.columns[0]
longitude_column = data.columns[1]
elevation_column = data.columns[2]

# 地図の中心を設定
center = [data[latitude_column].mean(), data[longitude_column].mean()]

# 基本地図を作成
m = folium.Map(center, zoom_start=6)

# ダウンロードしたCSVファイルの緯度、経度、標高データを使用してヒートマップレイヤーを追加する
heat_map = HeatMap(
    data=data[[latitude_column, longitude_column, elevation_column]].values,
    radius=15
).add_to(m)

# Streamlitで地図を表示
folium_static(m)
