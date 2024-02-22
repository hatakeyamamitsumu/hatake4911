import streamlit as st
import pandas as pd
import os
from streamlit_folium import folium_static
import folium
from folium import plugins

# Specify the main folder path
main_folder_path = "/mount/src/hatake4911/☆Webアプリ//CSVファイル各種/ヒートマップ地図用CSV/"

# List all subfolders in the main folder
subfolders = [f.path for f in os.scandir(main_folder_path) if f.is_dir()]

# Allow the user to select a subfolder
selected_subfolder = st.selectbox("サブフォルダを選択してください", subfolders)

# List all files in the selected subfolder
files_in_subfolder = [f for f in os.listdir(selected_subfolder) if f.endswith(".csv")]

# Allow the user to select a CSV file
selected_file = st.selectbox("CSVファイルを選択してください", files_in_subfolder)

# Construct the full file path
csv_file_path = os.path.join(selected_subfolder, selected_file)

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



