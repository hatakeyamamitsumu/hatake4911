import streamlit as st
from PIL import Image
import os
import random

st.title('Hat')
st.caption('こんにちは！Hatです。')
st.subheader('説明')
st.text('簡易なWEBアプリ「streamlit」を使って何かやろうと考えています。\nよろしくお願いします。')
st.text('')
# ハイパーリンクを表示するMarkdown文字列
link_str = "(https://forms.gle/DUHCTT5CfajGjoGMA)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('↑アンケートにお答えください。')
st.text('')
# フォルダのパス
image_folder_path = '/mount/src/hatake4911/☆Webアプリ/画像/東京画像'

# フォルダ内の画像ファイルのリストを取得
image_files = [f for f in os.listdir(image_folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]

# ランダムに一つの画像を選択
selected_image = random.choice(image_files)

# 選択された画像のフルパス
selected_image_path = os.path.join(image_folder_path, selected_image)



# 選択された画像を表示
st.text('こちらは2022年に東京に旅行した際の写真です。ランダムに表示されます。')
# 選択された画像のファイル名を表示
st.text(selected_image)
st.image(selected_image_path)

#code = '''
#cwd = os.getcwd()
#st.text(cwd)  # このコードによってgithub上のフルパスを確認
#'''
#st.code(code, language='python')
