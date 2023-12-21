import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from st_clickable_images import clickable_images
import base64
import pickle
from io import BytesIO
import glob
import os
from PIL import Image

st.set_config(title="投票",layout='wide')

