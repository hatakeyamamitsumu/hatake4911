import streamlit as st
from PIL import Image
import datetime
import pandas as pd
import os

code='''
cwd = os.getcwd()
st.text(cwd)#このコードによってgithub上のフルパスを確認
'''
st.code(code,language='python')




st.title('Hat')
st.caption('こんにちは！Hatです。')
st.subheader('説明')
st.text('簡易なWEBアプリ「streamlit」を使って何かやろうと考えています。\n'
       'よろしくお願いします。')

#フォルダ変更　　../images/my_image.jpg
#写真
st.text('こちらは2022年に東京に旅行した際の写真、動画です。')
#image=Image.open('skytree.png')
st.image('/mount/src/hatake4911/☆Webアプリ/画像/skytree.png',use_column_width=True)

# ローカルのGIFファイルのパスを指定
video_path = '/mount/src/hatake4911/☆Webアプリ/動画/東京到着.gif'
# 動画を表示
#st.video(video_path)
st.image(video_path)



