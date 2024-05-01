import streamlit as st
import folium

# 地図を表示する領域を指定
map_center = [35.6895, 139.6917]  # 東京の緯度経度

# 地図を表示
m = folium.Map(location=map_center, zoom_start=12)

# 地図上のクリックしたポイントの緯度経度を格納するリスト
clicked_points = []

# 地図上のクリックを検知するJavaScriptを生成
js_code = """
<script>
var map = document.getElementsByClassName('folium-map')[0];

// 地図上でクリックされたときの処理
map.on('click', function(event){
    var lat = event.latlng.lat.toFixed(6);
    var lng = event.latlng.lng.toFixed(6);
    var point = [lat, lng];
    // Streamlitにクリックしたポイントを送信
    Shiny.setInputValue('clicked_point', point);
});
</script>
"""

# Streamlitで地図を表示
st.markdown(folium.Map()._repr_html_(), unsafe_allow_html=True)
st.markdown(js_code, unsafe_allow_html=True)

# Streamlitでクリックしたポイントの緯度経度を受信して表示
clicked_point = st.empty()
clicked_point_info = st.empty()

# Streamlitでクリックしたポイントを受信して表示
clicked_point = st.empty()
clicked_point_info = st.empty()

while True:
    # Streamlitからクリックしたポイントを受信
    point = st.session_state.get('clicked_point')
    if point:
        clicked_points.append(point)
        clicked_point_info.write(f"クリックしたポイントの緯度経度: {point}")
