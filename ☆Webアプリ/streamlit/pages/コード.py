import streamlit as st
st.text("ページ2")
st.text('main_app.pyで使用したコード')
code='''
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
st.image('/mount/src/hatake4911/☆Webアプリ/画像/skytree.png',use_column_width=True)

# ローカルのGIFファイルのパスを指定
video_path = '/mount/src/hatake4911/☆Webアプリ/動画/東京到着.gif'
# 動画を表示
#st.video(video_path)
st.image(video_path)
'''
st.code(code,language='python')
st.text('当時の東京の天気.pyで使用したコード')
code='''
import streamlit as st
import pandas as pd
st.write("２０２２年１０月の東京の天気（気象庁より取得）")
st.write("https://www.data.jma.go.jp/stats/etrn/index.php")  
df = pd.read_csv("/mount/src/hatake4911/☆Webアプリ/csvファイル各種/２０２２年１０月の東京の天気.csv", encoding='shift_jis',index_col="日")
st.dataframe(df)

# 日ごとの平均気温と降水量を含む新しいデータフレームを作成
df_plot_temp = df[['平均気温(℃)']]
df_plot_rain = df[['降水量(mm)合計']]

# 降水量(mm)合計で昇順にソート
#df_plot_rain = df_plot_rain.sort_values(by='降水量(mm)合計', ascending=True)

# Streamlitで折れ線グラフと縦棒グラフを描画
st.line_chart(df_plot_temp,y='平均気温(℃)',use_container_width=True,height=400)


#st.bar_chart(df_plot_rain[::-1], use_container_width=True, height=400)
#st.bar_chart(df_plot_rain, use_container_width=True, height=400)
st.bar_chart(df_plot_rain,y="降水量(mm)合計" ,use_container_width=True, height=400)
'''
st.code(code,language='python')
