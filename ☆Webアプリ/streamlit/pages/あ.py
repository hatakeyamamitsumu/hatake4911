import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st
SP_CREDENTIAL_FILE = st.secrets["gcp"]["json_where"]
SP_SHEET_KEY = st.secrets["gcp"]["sheet_where"]
