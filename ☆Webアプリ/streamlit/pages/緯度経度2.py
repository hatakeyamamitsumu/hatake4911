import streamlit as st
import folium
from streamlit_folium import st_folium

# Define the data for the markers
data = [
    {"name": "Marker 1", "location": [35.6895, 139.6917]},
    {"name": "Marker 2", "location": [35.7119, 139.7003]},
    {"name": "Marker 3", "location": [35.7343, 139.7188]}
]

# Create a folium map
m = folium.Map(location=[35.6895, 139.6917], zoom_start=6)

# Add markers to the map
for marker_data in data:
    marker = folium.Marker(marker_data["location"], popup=marker_data["name"])
    marker.add_to(m)

# Define the click_event function
def click_event(click_location):
    # Add a new marker at the clicked location
    new_marker = folium.CircleMarker(click_location, radius=5, color='red')
    new_marker.add_to(m)

# Connect the click_event function to the map
m.on_click(click_event)

# Display the map in Streamlit
st_folium(m)
