import streamlit as st
from streamlit_folium import st_folium
import folium

# Initial values for latitude and longitude
initial_latitude = 35.6895  # Tokyo station latitude
initial_longitude = 139.6917  # Tokyo station longitude

# Create input fields for latitude and longitude
latitude_input = st.number_input('緯度', min_value=30, max_value=45, value=initial_latitude)
longitude_input = st.number_input('経度', min_value=130, max_value=145, value=initial_longitude)

# Create the map centered at the initial location
m = folium.Map(location=[initial_latitude, initial_longitude], zoom_start=7)

# Create a marker at the initial location
folium.Marker([initial_latitude, initial_longitude], popup='初期位置').add_to(m)

# Update the map and marker when input values change
def update_map():
    new_latitude = latitude_input
    new_longitude = longitude_input

    # Clear existing markers
    m.clear()

    # Create a new marker at the updated location
    folium.Marker([new_latitude, new_longitude], popup=f'新しい位置: {new_latitude}, {new_longitude}', color='red').add_to(m)

# Button to trigger map and marker update
update_button = st.button('更新')

# Update the map and marker when the button is clicked
if update_button:
    update_map()

# Display the map
st_folium(m)
