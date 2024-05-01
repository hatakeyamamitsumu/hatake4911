import streamlit as st
from streamlit_folium import st_folium
import folium

# Default values for latitude and longitude (assuming they're numerical)
initial_latitude = 35.6895  # Tokyo station latitude
initial_longitude = 139.6917  # Tokyo station longitude

# Combine latitude and longitude into a list (if necessary)
initial_location = [initial_latitude, initial_longitude]

# Create input fields for latitude and longitude
latitude_input = st.number_input('緯度', min_value=30, max_value=45, value=initial_latitude)
longitude_input = st.number_input('経度', min_value=130, max_value=145, value=initial_longitude)

# Create the map centered at the user-defined location
m = folium.Map(location=initial_location, zoom_start=7)

# Define a function to update the map and marker
def update_map():
    new_latitude = latitude_input
    new_longitude = longitude_input

    # Clear existing markers (optional, if you want to keep the initial marker, comment this out)
    m.clear()

    # Create a new marker at the updated location
    new_location = [new_latitude, new_longitude]
    folium.Marker(new_location, popup=f'新しい位置: {new_latitude}, {new_longitude}', color='red').add_to(m)

# Create a button to trigger the map and marker update
update_button = st.button('更新')

# Update the map and marker when the button is clicked
if update_button:
    update_map()

# Display the map
st_folium(m)
