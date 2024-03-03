import streamlit as st
from PIL import Image
import os
import random

st.title('Hat')
st.write('こんにちは！Hatと申します。。')

image_folder_path = '/mount/src/hatake4911/☆Webアプリ/画像/東京画像'
image_files = [f for f in os.listdir(image_folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
selected_image = random.choice(image_files)
selected_image_path = os.path.join(image_folder_path, selected_image)
st.text('こちらは2022年に東京に旅行した際の写真です。ランダムに表示されます。')
st.text(selected_image)
st.image(selected_image_path)


st.subheader('説明')
st.write('プログラミングは初心者ですが、簡易なWEBアプリ「streamlit」を使って何かできないかと考えて、発表し続けようと考えております。\nよろしくお願いします。')
st.text('オリジナルでないコードも含まれますが、可能な限り出典を明示させていただきます。')
st.text("")
# ハイパーリンクを表示するMarkdown文字列
link_str = "(https://forms.gle/DUHCTT5CfajGjoGMA)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('無記名アンケートです。差し支えなければお答えください。')
QR_path='/mount/src/hatake4911/☆Webアプリ/QRコード各種/アンケートフォーム用QR.png'
st.image(QR_path)




#code = '''
#cwd = os.getcwd()
#st.text(cwd)  # このコードによってgithub上のフルパスを確認
#'''
#st.code(code, language='python')
