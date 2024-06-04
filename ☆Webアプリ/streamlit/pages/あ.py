import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from io import BytesIO
import numpy as np

def main():
  # タイトルと説明を表示
  st.title("都道府県をデータをもとに塗り分け")
  st.write('様々な都道府県別データを集めて、値が大きい県ほど濃い色に塗られるように設定しています。')
  st.text('主に政府統計e-Statsより引用。')

  # 指定されたフォルダパス　CSVファイルと画像の表示
  folder_path = "/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/都道府県を塗り分け用ＣＳＶ/"

  # 指定されたフォルダ内のサブフォルダ一覧を取得
  subfolders = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]

  # サブフォルダが存在するか確認
  if not subfolders:
    st.warning("指定されたフォルダ内にサブフォルダが見つかりません。")
    return

  # サブフォルダの選択
  selected_subfolder = st.selectbox("フォルダを選択してください", subfolders)

  # 選択されたサブフォルダ内のすべての画像ファイル一覧を取得
  image_files = [file for file in os.listdir(os.path.join(folder_path, selected_subfolder))
                 if file.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

  # 画像が存在するか確認
  if not image_files:
    st.warning("選択されたフォルダ内に画像ファイルが見つかりません。")
    return

  # すべての画像を表示
  st.subheader("地図:")
  for selected_image in image_files:
    st.write(selected_image)
    image_path = os.path.join(folder_path, selected_subfolder, selected_image)
    image = Image.open(image_path)
    st.image(image, caption=f"{selected_image}", use_column_width=True)

  # 選択されたサブフォルダ内のすべてのCSVファイル一覧を取得
  csv_files = [file for file in os.listdir(os.path.join(folder_path, selected_subfolder)) if file.endswith('.csv')]

  # CSVファイルが存在するか確認
  if not csv_files:
    st.warning("選択されたフォルダ内にCSVファイルが見つかりません。")
    return

  # すべてのCSVファイルを表示
  st.subheader("塗分けに使った資料の内容:")
  for selected_csv in csv_files:
    st.write(selected_csv)
    csv_path = os.path.join(folder_path, selected_subfolder, selected_csv)
    df = pd.read_csv(csv_path)
    st.dataframe(df)

  # データを取得
  df = pd.read_csv(csv_path)

  # 緯度経度リストを作成
  lat_lon_list = list(zip(df["緯度"], df["経度"]))

  # 平均値を計算
  lat_avg = df["緯度"].mean()
  lon_avg = df["経度"].mean()

  # 地図を作成
  m = folium.Map(location=[lat_avg, lon_avg], zoom_start=6)

  # 塗り分けデータを作成
  data = np.array(df["値"])

  # ヒートマップを作成
  HeatMap(data, lat_lon_list, radius=25, max_opacity=1, gradient_colors=colMap).add_to(m)

  # 縮尺コントロールを追加
  folium.ZoomControl().add_to(m)

  # 全画面表示ボタンを追加
  folium.FullScreen().add_to(m)

  # 保存
  map_data = BytesIO()
  
