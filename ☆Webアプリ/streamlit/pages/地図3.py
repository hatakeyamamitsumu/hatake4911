import folium
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_folium import folium_static, st_folium
import pandas as pd

# Google Sheetsの認証情報
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json", scope)
client = gspread.authorize(creds)

# アプリ選択
app_selection = st.sidebar.radio("アプリを選択してください", ("地図にピンを立て、コメントをつけて保存する", "スプレッドシートから地図上に表示"))

if app_selection == "地図にピンを立て、コメントをつけて保存する":
    # タイトルを設定
    st.title("地図にピンを立て、コメントをつけて保存するアプリ")
    st.write("※緯度経度の0.0001度は、おおよそ10メートルです。")
    # 地図の拡大率の設定
    zoom_value = st.slider("地図の拡大率を固定したい時は、このスライダーをご利用ください", min_value=1, max_value=20, value=10)
    # 緯度の入力方法を選択
    latitude_input = st.sidebar.number_input("緯度を入力してください", value=35.6895, step=0.0001, format="%.4f", key="latitude")
    longitude_input = st.sidebar.number_input("経度を入力してください", value=139.6917, step=0.0001, format="%.4f", key="longitude")

    # ユーザーから情報の入力を受け取る
    info = st.sidebar.text_input("コメントを入力してください")

    # 地図を作成
    m = folium.Map(location=[latitude_input, longitude_input], zoom_start=zoom_value, zoom_control=False)  # 拡大縮小ボタンを非表示
    # 入力された緯度経度にピンを立てる
    folium.Marker([latitude_input, longitude_input], popup=folium.Popup(info, max_width=300)).add_to(m)

    # 地図を表示して、クリックイベントを取得
    folium_map = st_folium(m, width=700, height=500)

    # 地図クリック時の緯度経度をサイドバーに表示
    if folium_map['last_clicked'] is not None:
        st.sidebar.write(f"クリックされた位置: {folium_map['last_clicked']}")
        st.sidebar.number_input("緯度を入力してください", value=folium_map['last_clicked']['lat'], step=0.0001, format="%.4f", key="latitude")
        st.sidebar.number_input("経度を入力してください", value=folium_map['last_clicked']['lng'], step=0.0001, format="%.4f", key="longitude")

    # Google DriveのファイルID
    file_id = "1fDInJTb7My6by9Dx70XIByDh8yux-09i"

    # ファイルを読み込む
    @st.cache_data
    def load_data(file_id):
        url = f"https://drive.google.com/uc?id={file_id}"
        return pd.read_csv(url)

    # Streamlitアプリのセットアップ
    def main():
        st.title("おおよその緯度経度検索")

        # CSVファイルを読み込む
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

    # Streamlitアプリを実行
    if __name__ == "__main__":
        main()
    # 書き込みボタンを追加
    if st.sidebar.button("緯度経度、コメントを保存"):
        # Google Sheetsのデータを取得
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1X1mppebuIXGIGd-n_9pL6wHahk1-rFbO2tAjgc9mEqg/edit?usp=drive_link"
        sheet = client.open_by_url(spreadsheet_url).sheet1

        # 新しいデータをGoogle Sheetsに書き込む
        new_row = [latitude_input, longitude_input, info]
        sheet.append_row(new_row)

        # ユーザーに成功メッセージを表示
        st.sidebar.success("情報と緯度経度がGoogle Sheetsに書き込まれました。")

elif app_selection == "スプレッドシートから地図上に表示":
    # タイトルを設定
    st.title("スプレッドシートから地図上に表示")

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

    # 地図を表示
    folium_static(m)
