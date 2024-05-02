import folium
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_folium import folium_static

# Google Sheetsの認証情報
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json", scope)  
client = gspread.authorize(creds)

# タイトルを設定
st.title("スプレッドシートから地図上に表示")

# スプレッドシートのURLを入力
spreadsheet_url = st.text_input("スプレッドシートのURLを入力してください")

# スプレッドシートのシートを選択
sheet_name = st.text_input("シート名を入力してください")

# スプレッドシートからデータを取得
if spreadsheet_url and sheet_name:
    try:
        sheet = client.open_by_url(spreadsheet_url).worksheet(sheet_name)
        data = sheet.get_all_values()

        # 地図を作成
        m = folium.Map()

        # データから緯度経度を取得し、ピンを立てる
        for row in data[1:]:  # ヘッダーを除く
            latitude, longitude, info = float(row[0]), float(row[1]), row[2]
            folium.Marker([latitude, longitude], popup=info).add_to(m)

        # 地図を表示
        folium_static(m)
    except gspread.exceptions.APIError as e:
        st.error("スプレッドシートが見つかりません。正しいURLとシート名を入力してください。")
