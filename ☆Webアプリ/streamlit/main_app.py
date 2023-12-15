import streamlit as st
from PIL import Image
import datetime
import pandas as pd
import os
df = pd.DataFrame
st.title('Hatake')
st.caption('こんにちは！Hatakeです。')
st.subheader('説明')
st.text('簡易なWEBアプリ「streamlit」を使って何かやろうと考えています。\n'
       'よろしくお願いします。')
cwd = os.getcwd()
st.text(cwd)
#フォルダ変更　　../images/my_image.jpg
#写真
st.text('こちらは2022年に東京に旅行した際の写真、動画です。')
#image=Image.open('skytree.png')
st.image('skytree.png',use_column_width=True)
video_file=open('../動画/東京到着.mp4','rb')

video_bytes=video_file.read()

st.video(video_bytes)

with st.form(key='profile_form'):

    name=st.text_input('名前')
    adderess=st.text_input('住所')

    age_category=st.selectbox(
    '年齢層',
    ("子供（18歳未満）","大人（18歳以上）")
    )
    hobby=st.multiselect("趣味",("スポーツ","読書","釣り","料理","音楽","ダンス","手芸","日曜大工","ゲーム"))
    
    checkbox=st.checkbox('定期的に閲覧する')
    height=st.slider('身長',min_value=110,max_value=210)
    start_date=st.date_input('開始日を入力してください：',datetime.date(2024,1,1))
    submit_bottun=st.form_submit_button('送信')
    cancel_bottun=st.form_submit_button('キャンセル')
    selected_color=st.color_picker('好きな色','#00f900')

    if submit_bottun:
        st.text(f'こんにちは、{adderess}在住の{name}さん！')
        st.text(f'年齢層：{age_category}')
        st.text(f'趣味：{",".join(hobby)}')
        st.text(f'定期的に閲覧する：{checkbox}')
        st.text(f'身長：{height}cm')
        st.text(f'開始日：{start_date}')
        st.write(f'選択した色: {selected_color}')
        
st.text('売上管理')      
df2=pd.read_csv("../csvファイル各種/4-4_sales.csv")

st.dataframe(df2)
# 特定の列を指定して折れ線グラフを描画
st.line_chart(df2)
st.bar_chart(df2['sales'])
#WEB上にコードを表示できるようになります
st.text('使用したコード')
code='''
import streamlit as st
from PIL import Image
st.title('Hatake')
st.caption('こんにちは！Hatakeです。')
st.subheader('説明')
st.text('簡易なWEBアプリ「streamlit」を使って何かやろうと考えています。\n'
       'よろしくお願いします。')

#写真
st.text('こちらは2022年に東京に旅行した際の写真、動画です。')
image=Image.open('./写真/スカイツリー遠景.jpg')
st.image(image,width=300)
video_file=open('./動画/東京到着.mp4','rb')

video_bytes=video_file.read()

st.video(video_bytes)
'''
st.code(code,language='python')
