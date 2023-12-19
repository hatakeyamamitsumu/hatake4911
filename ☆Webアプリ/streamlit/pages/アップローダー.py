import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(page_title='csvファイル',layout='centered')
st.title('CSVファイルのアップロードと読み込み1')
uploaded_file=st.file_uploader('utf-8 CSV',type='csv',key='csv')

if uploaded_file:
  df=pd.read_csv(uploaded_file,encoding='utf-8')
  st.markdown('#### dataframe')
  st.dataframe(df)


st.title('CSVファイルのアップロードと読み込み2')
uploaded_file=st.file_uploader('shift-jis CSV',type='csv',key='csv')

if uploaded_file:
  df=pd.read_csv(uploaded_file,encoding='shift-jis')
  st.markdown('#### dataframe')
  st.dataframe(df)
