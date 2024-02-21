import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from folium import plugins

# Read data from CSV file
csv_file_path = "/mount/src/hatake4911/☆Webアプリ//CSVファイル各種/ヒートマップ地図用CSV/標高情報.csv"
data = pd.read_csv(csv_file_path)

# Check if the data has latitude, longitude, and elevation columns
required_columns = ['緯度', '経度', '標高']
missing_columns = [col for col in required_columns if col not in data.columns]

# Display a warning if any required columns are missing
if missing_columns:
    st.warning(f"CSVファイルに必要な列が不足しています。不足している列: {', '.join(missing_columns)}")
else:
    # Center of the map (you may adjust this based on your data)
    center = [data['緯度'].mean(), data['経度'].mean()]

    # Create a base map
    m = folium.Map(center, zoom_start=6)

    # Add a heatmap layer to the map using the latitude, longitude, and elevation data from the CSV
    heat_map = folium.plugins.HeatMap(
        data=data[['緯度', '経度', '標高']].values,  # Use the latitude, longitude, and elevation columns
        radius=15  # You can adjust the radius of the heatmap points
    ).add_to(m)

    # Add markers with popups for each point, and customize the icon size
    #icon='flag','map-marker','flag','star','circle'
    for index, row in data.iterrows():
        popup_text = f"標高: {row['標高']} m"
        folium.Marker(
            location=[row['緯度'], row['経度']],
            popup=popup_text,
            icon=folium.Icon(icon='circle', color='blue', prefix='fa', icon_size=(15, 15))  # Adjust the icon_size
        ).add_to(m)

    # Display the map using Streamlit
    st.header("ヒートマップの例")
    folium_static(m)
