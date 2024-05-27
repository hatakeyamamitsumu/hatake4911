import folium
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from folium.plugins import MousePosition
from streamlit_folium import folium_static, st_folium
import pandas as pd
#
# Google Sheets 認証情報とスコープをsecretsから取得
scope = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
client = gspread.authorize(creds)
file_id = "1fDInJTb7My6by9Dx70XIByDh8yux-09i"

# アプリ選択
app_selection = st.sidebar.radio("アプリを選択してください", ("地図にピンを立て、コメントをつけて保存する", "スプレッドシートから地図上に表示"))

if app_selection == "地図にピンを立て、コメントをつけて保存する":
    # タイトルを設定
    st.title("地図にピンを立て、コメントをつけて保存するアプリ")
    # 地図の拡大率の設定
    zoom_value = st.slider("地図の倍率(遠⇔近)", min_value=7, max_value=20, value=10)
    # 緯度の入力方法を選択。
    latitude_slider = st.sidebar.slider("おおよその緯度指定", min_value=23.2100, max_value=46.3200, value=35.0000, step=0.001)
    latitude_input = st.sidebar.number_input("南北に１００ｍ移動　(緯度コピペ欄)",value=latitude_slider,step=0.001,format="%.4f",key="latitude")

    
    longitude_slider = st.sidebar.slider("おおよその経度指定", min_value=121.5500, max_value=146.0800, value=135.0000, step=0.001)
    longitude_input = st.sidebar.number_input("東西に１００ｍ移動　(経度コピペ欄)",value=longitude_slider,step=0.001,format="%.4f",key="longitude")
    # ユーザーから情報の入力を受け取る
    info = st.sidebar.text_input("ピンに添えるコメントを入力してください")
    # 地図を作成
    #m = folium.Map(location=[latitude_input, longitude_input], zoom_start=zoom_value, zoom_control=False)  # 拡大縮小ボタンを非表示
    # 入力された緯度経度にピンを立てる
    #folium.Marker([latitude_input, longitude_input], popup=folium.Popup(info, max_width=300)).add_to(m)
    # 地図を表示
    ###########
     # 地図を作成
    #MousePosition(position='bottomright', separator=' | ', prefix="マウス位置：").add_to(m)
    # フォリウムのクリックイベントを追加
    click_event = folium.ClickForMarker(popup=folium.Popup("ここです！", max_width=300))
    m.add_child(click_event)
    # Streamlitで地図を表示し、クリックイベントを取得
    output = st_folium(m, width=700, height=500)
    # 入力された緯度経度にピンを立てる
    folium.Marker([latitude_input, longitude_input], popup=folium.Popup(info, max_width=600), icon=folium.Icon(color='blue')).add_to(m)
    # 地図を表示
    # 地図を表示
    #folium_static(m)
    #########
    folium_static(m)
    # Google DriveのファイルID
    file_id = "1fDInJTb7My6by9Dx70XIByDh8yux-09i"
     # ファイルを読み込む
    @st.cache
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
