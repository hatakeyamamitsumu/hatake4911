



import streamlit as st
import pandas as pd
import os
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from streamlit_folium import folium_static
import folium
from folium import plugins

st.header("グーグルドライブ内のCSVデータをもとにヒートマップを表示")
st.text('主に国土地理院データより引用。')

# Google Drive APIの認証情報

scope = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
credentials = Credentials.from_service_account_info(st.secrets["google"], scopes=scope)
client = gspread.authorize(creds)
#file_id = "1fDInJTb7My6by9Dx70XIByDh8yux-09i"
service = build('drive', 'v3', credentials=credentials)

# Google Drive folder ID
drive_folder_id = "1f3XeJDSoEydQHkw867Mt26NUGe2MPJJ1"

# Function to list files in Google Drive folder
def list_drive_files(folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query).execute()
    files = results.get('files', [])
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

# Download the selected CSV file
file_url = f"https://drive.google.com/uc?id={selected_file_id}"
csv_file_path = f"/tmp/{selected_file_name}"
response = requests.get(file_url)
with open(csv_file_path, 'wb') as f:
    f.write(response.content)

# Read data from the downloaded CSV file
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
