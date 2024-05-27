import folium
from folium.plugins import MousePosition
import streamlit as st
from streamlit_folium import folium_static

# 地図を作成
latitude = 35.0
longitude = 135.0
zoom_start = 10

# 地図オブジェクトを作成
m = folium.Map(location=[latitude, longitude], zoom_start=zoom_start)

# MousePositionプラグインを追加
mouse_position = MousePosition(
    position='topright',  # マウス位置表示の位置
    separator=' Long: ',  # 緯度経度の区切り
    empty_string='マウスを動かしてください',  # 初期表示
    lng_first=False,  # 経度を先に表示するかどうか
    num_digits=5,  # 小数点以下の桁数
    prefix='Lat: ',  # 緯度の前に表示するテキスト
    lat_formatter=None,  # 緯度のフォーマット
    lng_formatter=None,  # 経度のフォーマット
)
mouse_position.add_to(m)

# Streamlitで地図を表示
folium_static(m)
