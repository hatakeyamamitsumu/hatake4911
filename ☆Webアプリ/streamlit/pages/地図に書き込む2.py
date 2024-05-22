import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

# アプリ選択
app_selection = st.sidebar.radio("アプリを選択してください", ("地図にピンを立て、コメントをつけて保存する", "スプレッドシートから地図上に表示"))

if app_selection == "地図にピンを立て、コメントをつけて保存する":
    # タイトルを設定
    st.title("地図にピンを立て、コメントをつけて保存するアプリ")
    st.write("※緯度経度の0.000001度は、おおよそ0.1メートルです。")
    # 地図の拡大率の設定
    zoom_value = st.slider("地図の拡大率を固定したい時は、このスライダーをご利用ください", min_value=1, max_value=20, value=10)

    # 緯度の入力方法を選択
    with st.sidebar.expander("緯度を選択してください"):
        latitude_input = st.number_input("緯度を入力してください", value=35.689500, step=0.000001, format="%.6f", key="latitude")

    # 経度の入力方法を選択
    with st.sidebar.expander("経度を選択してください"):
        longitude_input = st.number_input("経度を入力してください", value=139.691700, step=0.000001, format="%.6f", key="longitude")

    # ユーザーから情報の入力を受け取る
    # ユーザーから情報の入力を受け取る
    info = st.sidebar.text_area("コメントを入力してください")


    # 地図を作成
    m = folium.Map(location=[latitude_input, longitude_input], zoom_start=zoom_value, zoom_control=False)  # 拡大縮小ボタンを非表示
    # 入力された緯度経度にピンを立てる
    folium.Marker([latitude_input, longitude_input], popup=folium.Popup(info, max_width=300)).add_to(m)

    # 地図を表示
    folium_static(m)

elif app_selection == "スプレッドシートから地図上に表示":
    # タイトルを設定
    st.title("スプレッドシートから地図上に表示")

    # スプレッドシートのURL
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1X1mppebuIXGIGd-n_9pL6wHahk1-rFbO2tAjgc9mEqg/edit?usp=drive_link"

    # スプレッドシートからシート名を取得
    sheet_names = pd.read_html(spreadsheet_url)[0]['Sheet1'].tolist()

    # シート名を選択
    selected_sheet_name = st.selectbox("シート名を選択してください", sheet_names)

    # スプレッドシートからデータを取得
    df = pd.read_html(spreadsheet_url, sheet_name=selected_sheet_name)[0]

    # 地図を作成
    m = folium.Map()

    # データから緯度経度を取得し、ピンを立てる
    for index, row in df.iterrows():
        latitude, longitude, info = float(row["緯度"]), float(row["経度"]), row["コメント"]
        folium.Marker([latitude, longitude], popup=folium.Popup(info, max_width=300)).add_to(m)

    # 地図を表示
    folium_static(m)
