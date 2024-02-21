import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from folium import plugins

# Read data from CSV file
data = pd.read_csv("/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/標高情報.csv")

# Center of the map (you may adjust this based on your data)
center = [data['緯度'].mean(), data['経度'].mean()]

# Create a base map
m = folium.Map(center, zoom_start=6)

# Add a heatmap layer to the map using the latitude, longitude, and elevation data from the CSV
folium.plugins.HeatMap(
    data=data[['緯度', '経度', '標高']].values,  # Use the latitude, longitude, and elevation columns
    radius=15  # You can adjust the radius of the heatmap points
).add_to(m)

# Display the map using Streamlit
st.header("ヒートマップの例")
folium_static(m)
