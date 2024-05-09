import folium
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_folium import folium_static

# Google Sheetsの認証情報
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("/mount/src/hatake4911/☆Webアプリ/その他/gspread-test-421301-6cd8b0cc0e27.json", scope)  
client = gspread.authorize(creds)

# アプリ選択
app_selection = st.sidebar.radio("アプリを選択してください", ("地図にピンを立て、コメントをつけて保存する", "スプレッドシートから地図上に表示"))

if app_selection == "地図にピンを立て、コメントをつけて保存する":
    # タイトルを設定
    st.title("地図にピンを立て、コメントをつけて保存するアプリ")
    st.write("※緯度経度の0.000001度は、おおよそ0.1メートルです。")
    # 地図の拡大率の設定
    zoom_value = st.slider("地図の拡大率を固定したい時は、このスライダーをご利用ください", min_value=1, max_value=20, value=10)
    # 緯度の入力方法を選択
    latitude_slider = st.sidebar.slider("緯度を選択してください", min_value=-90.000000, max_value=90.000000, value=35.689500, step=0.000001)
    latitude_input = st.sidebar.number_input("緯度を入力してください", value=latitude_slider, step=0.000001, format="%.6f", key="latitude")

    # 経度の入力方法を選択
    longitude_slider = st.sidebar.slider("経度を選択してください", min_value=-180.000000, max_value=180.000000, value=139.691700, step=0.000001)
    longitude_input = st.sidebar.number_input("経度を入力してください", value=longitude_slider, step=0.000001, format="%.6f", key="longitude")

    # ユーザーから情報の入力を受け取る
    info = st.sidebar.text_input("コメントを入力してください")

    # 地図を作成
    m = folium.Map(location=[latitude_input, longitude_input], zoom_start=zoom_value)

    # 入力された緯度経度にピンを立てる
    folium.Marker([latitude_input, longitude_input], popup=info).add_to(m)

    # 地図を表示
    folium_static(m)

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
        folium.Marker([latitude, longitude], popup=info).add_to(m)

    # 地図を表示
    folium_static(m)


# データの準備
st.wtrite("参考資料：")
data = {
    "県名": ["北海道（札幌市）", "青森県（青森市）", "岩手県（盛岡市）", "宮城県（仙台市）", "秋田県（秋田市）",
           "山形県（山形市）", "福島県（福島市）", "茨城県（水戸市）", "栃木県（宇都宮市）", "群馬県（前橋市）",
           "埼玉県（さいたま市）", "千葉県（千葉市）", "東京都（東京）", "神奈川県（横浜市）", "新潟県（新潟市）",
           "富山県（富山市）", "石川県（金沢市）", "福井県（福井市）", "山梨県（甲府市）", "長野県（長野市）",
           "岐阜県（岐阜市）", "静岡県（静岡市）", "愛知県（名古屋市）", "三重県（津市）", "滋賀県（大津市）",
           "京都府（京都市）", "大阪府（大阪市）", "兵庫県（神戸市）", "奈良県（奈良市）", "和歌山県（和歌山市）",
           "鳥取県（鳥取市）", "島根県（松江市）", "岡山県（岡山市）", "広島県（広島市）", "山口県（山口市）",
           "徳島県（徳島市）", "香川県（高松市）", "愛媛県（松山市）", "高知県（高知市）", "福岡県（福岡市）",
           "佐賀県（佐賀市）", "長崎県（長崎市）", "熊本県（熊本市）", "大分県（大分市）", "宮崎県（宮崎市）",
           "鹿児島県（鹿児島市）", "沖縄県（那覇市）"],
    "緯度": [43.03, 40.49, 39.42, 38.16, 39.43, 38.15, 37.45, 36.22, 36.33, 36.23,
           35.51, 35.36, 35.41, 35.27, 37.54, 36.41, 36.33, 36.03, 35.39, 36.39,
           35.25, 34.58, 35.11, 34.43, 35.01, 35.00, 34.41, 34.41, 34.41, 34.14,
           35.21, 35.28, 34.39, 34.23, 34.11, 34.04, 34.20, 33.50, 33.33, 33.35,
           33.16, 32.46, 32.48, 33.14, 31.54, 31.36, 26.13],
    "経度": [141.21, 140.44, 141.09, 140.52, 140.06, 140.20, 140.28, 140.28, 139.52, 139.03,
           139.38, 140.06, 139.41, 139.38, 139.02, 137.13, 136.39, 136.13, 138.34, 138.11,
           136.46, 138.23, 136.54, 136.30, 135.52, 135.46, 135.30, 135.11, 135.49, 135.10,
           134.14, 133.04, 133.55, 132.27, 131.28, 134.33, 134.02, 132.47, 133.32, 130.23,
           130.18, 129.52, 130.41, 131.36, 131.25, 130.33, 127.41]
}

df = pd.DataFrame(data)

# Streamlitで表示
st.write(df)

