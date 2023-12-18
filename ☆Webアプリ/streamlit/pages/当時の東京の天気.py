import streamlit as st
import pandas as pd
st.write("２０２２年１０月の東京の天気")
   
df = pd.read_csv("/mount/src/hatake4911/☆Webアプリ/csvファイル各種/２０２２年１０月の東京の天気.csv", encoding='shift_jis',index_col=None)

st.dataframe(df)
