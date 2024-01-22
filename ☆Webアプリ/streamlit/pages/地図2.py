import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.title('Osaka Precipitation')

# LOAD DATA ONCE
@st.experimental_singleton
def load_data():
    data = pd.read_csv(
        "/mount/src/hatake4911/☆Webアプリ/CSVファイル各種/地図用CSV/標高.csv",
        nrows=825,
        names=[
            "緯度",
            "経度"
        ],
        
        usecols=[2, 3],  # 3、4列目を使用する
    )
    return data


# FUNCTION FOR AIRPORT MAPS
def map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v8",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 10,
            },
            layers=[
                pdk.Layer(
                    'HexagonLayer',
                    data=data,
                    get_position='[lon, lat]',
                    radius=750,
                    elevation_scale=4,
                    elevation_range=[0, 5000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )


# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.experimental_memo
def mpoint(lat, lon):
    return np.average(lat), np.average(lon)


# STREAMLIT APP LAYOUT
data = load_data()

# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
zoom_level = 12
midpoint = mpoint(data["緯度], data["経度"])
map(data, midpoint[0], midpoint[1], 8.5)
