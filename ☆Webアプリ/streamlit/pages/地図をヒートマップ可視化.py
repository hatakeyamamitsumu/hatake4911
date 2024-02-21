import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from folium import plugins

# Read data from CSV file
csv_file_path = "/mount/src/hatake4911/☆Webアプリ//CSVファイル各種/ヒートマップ地図用CSV/標高情報.csv"
data = pd.read_csv(csv_file_path)

# Check if the data has latitude, longitude, and elevation columns
latitude_column = data.columns[0]
longitude_column = data.columns[1]
elevation_column = data.columns[2]

# Center of the map (you may adjust this based on your data)
center = [data[latitude_column].mean(), data[longitude_column].mean()]

# Create a base map
m = folium.Map(center, zoom_start=6)

# Add a heatmap layer to the map using the latitude, longitude, and elevation data from the CSV
heat_map = folium.plugins.HeatMap(
    data=data[[latitude_column, longitude_column, elevation_column]].values,  # Use the latitude, longitude, and elevation columns
    radius=15  # You can adjust the radius of the heatmap points
).add_to(m)

# Add markers with popups for each point, and customize the icon size
# icon='flag', 'map-marker', 'flag', 'star', 'circle'
for index, row in data.iterrows():
    popup_text = f"{elevation_column}: {row[elevation_column]} "
    folium.Marker(
        location=[row[latitude_column], row[longitude_column]],
        popup=popup_text,
        icon=folium.Icon(icon='circle', color='blue', prefix='fa', icon_size=(15, 15))  # Adjust the icon_size
    ).add_to(m)

# Display the map using Streamlit
st.header("ヒートマップ")
folium_static(m)

