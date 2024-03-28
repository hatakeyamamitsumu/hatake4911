import streamlit as st
import pandas as pd
import os
from streamlit_folium import folium_static
import folium
from folium import plugins

st.header("CSVデータをもとにヒートマップを表示")
st.text('主に国土地理院データより引用。')

# Allow the user to select a folder
folder_path = st.sidebar.selectbox("フォルダを選択してください", os.listdir("/mount/src/hatake4911/☆Webアプリ//CSVファイル各種/ヒートマップ地図用CSV"))

# Construct the full folder path
folder_full_path = os.path.join("/mount/src/hatake4911/☆Webアプリ//CSVファイル各種/ヒートマップ地図用CSV", folder_path)

# List all CSV files in the selected folder
csv_files = [f for f in os.listdir(folder_full_path) if f.endswith(".csv")]

# Allow the user to select a CSV file
selected_file = st.selectbox("CSVファイルを選択してください", csv_files)

# Construct the full file path
csv_file_path = os.path.join(folder_full_path, selected_file)

# Read data from the selected CSV file
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

# Display the map using Streamlit
folium_static(m)
