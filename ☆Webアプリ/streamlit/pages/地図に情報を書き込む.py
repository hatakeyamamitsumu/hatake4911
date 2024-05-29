import folium
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from folium.plugins import MousePosition
from streamlit_folium import folium_static, st_folium
import pandas as pd

# Google Sheets 認証情報とスコープをsecretsから取得
scope = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
client = gspread.authorize(creds)
file_id = "1fDInJTb7My6by9Dx70XIByDh8yux-09i"

# セッション状態にクリックされた位置の緯度と経度を保存
if "latitude" not in st.session_state:
    st.session_state.latitude = 35.0000
if "longitude" not in st.session_state:
    st.session_state.longitude = 135.0000

# アプリ選択
app_selection = st.sidebar.radio("アプリを選択してください", ("地図のおすすめスポットにピンを立てる", "地図上のすべてのピンを表示"))

if app_selection == "地図のおすすめスポットにピンを立てる":
    # タイトルを設定
    st.title("地図にピンを立て、コメントをつけて保存できます。")
    st.write("地図を動かす：左ドラッグ　ピンを立てる：左クリック")
    # 緯度と経度の入力欄
    latitude_input = st.sidebar.number_input("緯度を入力してください", value=st.session_state.latitude, step=0.001, format="%.4f", key="latitude_input")
    longitude_input = st.sidebar.number_input("経度を入力してください", value=st.session_state.longitude, step=0.001, format="%.4f", key="longitude_input")

    # ユーザーから情報の入力を受け取る
    info = st.sidebar.text_input("ピンに添えるコメントを入力してください")

    # 地図を作成
    m = folium.Map(location=[latitude_input, longitude_input], zoom_start=10)
    folium.Marker([latitude_input, longitude_input], popup=folium.Popup(info, max_width=300)).add_to(m)

    # MousePositionプラグインを追加して現在の座標を表示
    MousePosition(position='topleft', separator=' | ', prefix="現在の座標：").add_to(m)
    
    # LatLngPopupプラグインを追加してクリック位置を表示
    m.add_child(folium.LatLngPopup())

    # 地図を表示してクリックイベントを処理
    result = st_folium(m, width=700, height=500, returned_objects=["last_clicked"])

    # クリックした位置の緯度経度をセッション状態に保存
    if result and result.get("last_clicked"):
        st.session_state.latitude = result["last_clicked"]["lat"]
        st.session_state.longitude = result["last_clicked"]["lng"]
        st.experimental_rerun()  # ウィジェットの値を更新するためにページをリロード

    # 書き込みボタンを追加
    if st.sidebar.button("緯度経度、コメントを保存"):
        # Google Sheetsのデータを取得
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1X1mppebuIXGIGd-n_9pL6wHahk1-rFbO2tAjgc9mEqg/edit?usp=drive_link"
        sheet = client.open_by_url(spreadsheet_url).sheet1

        # 新しいデータをGoogle Sheetsに書き込む
        new_row = [st.session_state.latitude, st.session_state.longitude, info]
        sheet.append_row(new_row)

        # ユーザーに成功メッセージを表示
        st.sidebar.success("情報と緯度経度がGoogle Sheetsに書き込まれました。")

    def search_coordinates():
        st.title("おおよその緯度経度検索")
    
        # CSVファイルを読み込む
        file_id = "1fDInJTb7My6by9Dx70XIByDh8yux-09i"
        df = load_data(file_id)
        # 都道府県名の入力欄
        prefecture = st.text_input("都道府県名を入力してください：")
            
        # 市区町村名の入力欄
        city = st.text_input("市区町村名を入力してください：")
            
        # 大字・丁目名の入力欄
        district = st.text_input("大字・丁目名を入力してください：")
            
        # 部分一致検索を実行
        if prefecture or city or district:
            filtered_df = df[df["都道府県名"].str.contains(prefecture) &
                            df["市区町村名"].str.contains(city) &
                            df["大字・丁目名"].str.contains(district)]
            st.write(filtered_df)
    search_coordinates()







elif app_selection == "地図上のすべてのピンを表示":
    # タイトルを設定
    st.title("地図上のすべてのピンを表示")

    # スプレッドシートのURL
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1X1mppebuIXGIGd-n_9pL6wHahk1-rFbO2tAjgc9mEqg/edit?usp=drive_link"
    # スプレッドシートからシート名を取得
    spreadsheet = client.open_by_url(spreadsheet_url)
    sheet_names = [sheet.title for sheet in spreadsheet.worksheets()]

    # シート名を選択
    selected_sheet_name = st.selectbox("シート名を選択してください", sheet_names)

    # スプレッドシートからデータを取得
    sheet = spreadsheet.worksheet(selected_sheet_name)
    data = sheet.get_all_values()

    # 地図を作成
    m = folium.Map()

    # データから緯度経度を取得し、ピンを立てる
    for row in data[1:]:  # ヘッダーを除く
        latitude, longitude, info = float(row[0]), float(row[1]), row[2]
        folium.Marker([latitude, longitude], popup=folium.Popup(info, max_width=300)).add_to(m)

    # MousePositionプラグインを追加して現在の座標を表示
    MousePosition(position='bottomright', separator=' | ', prefix="現在の座標：").add_to(m)

    # 地図を表示
    folium_static(m)





