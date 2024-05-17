import streamlit as st
import pandas as pd
import os
import gdown
from streamlit_folium import folium_static
import folium
from folium import plugins

st.header("CSVデータをもとにヒートマップを表示")
st.text('主に国土地理院データより引用。')

# Google Drive folder ID
drive_folder_id = "your_google_drive_folder_id_here"

# Function to list files in Google Drive folder
def list_drive_files(folder_id):
    query = f"'{folder_id}' in parents"
    url = f"https://www.googleapis.com/drive/v3/files?q={query}&key=your_api_key"
    response = requests.get(url)
    files = response.json().get('files', [])
    return files

# Get the list of folders in the specified Google Drive folder
folders = list_drive_files(drive_folder_id)
folder_names = [folder['name'] for folder in folders]
folder_ids = {folder['name']: folder['id'] for folder in folders}

# Allow the user to select a folder
selected_folder_name = st.selectbox("フォルダを選択してください", folder_names)
selected_folder_id = folder_ids[selected_folder_name]

# Get the list of CSV files in the selected folder
csv_files = list_drive_files(selected_folder_id)
csv_file_names = [file['name'] for file in csv_files if file['name'].endswith('.csv')]
csv_file_ids = {file['name']: file['id'] for file in csv_files if file['name'].endswith('.csv')}

# Allow the user to select a CSV file
selected_file_name = st.selectbox("CSVファイルを選択してください", csv_file_names)
selected_file_id = csv_file_ids[selected_file_name]

# Download the selected CSV file using gdown
gdown.download(f"https://drive.google.com/uc?id={selected_file_id}", f"/tmp/{selected_file_name}", quiet=False)

# Read data from the downloaded CSV file
data = pd.read_csv(f"/tmp/{selected_file_name}")

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
