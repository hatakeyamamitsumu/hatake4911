import folium
from folium.plugins import HeatMap

# 緯度と経度の情報
latitudes = [35.652832, 35.658581, 35.660333]
longitudes = [139.839478, 139.840439, 139.836389]

# 地図の作成
map_center = [sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)]
my_map = folium.Map(location=map_center, zoom_start=15)

# ヒートマップの生成
heat_data = [[lat, lon] for lat, lon in zip(latitudes, longitudes)]
HeatMap(heat_data).add_to(my_map)

# 地図の表示
my_map.save("heatmap.html")

