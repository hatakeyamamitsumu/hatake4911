import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(page_title='csvファイル',layout='centered')
st.title('CSVファイルのアップロードと読み込み')
uploaded_file=st.fole_uploader('file of CSV',type='csv',key='csv')

if uploaded_file:
  df=pd.read_csv(uploaded_file,encoding='utf-8')
  st.markdown('#### dataframe')
  st.dataframe(df)
