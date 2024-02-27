import streamlit as st
# ハイパーリンクを表示するMarkdown文字列
link_str = "(https://forms.gle/DUHCTT5CfajGjoGMA)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('↑アンケートにお答えください。')
QR_path='mount/src/hatake4911/☆Webアプリ/画像/QRコード/アンケート用グーグルフォームのQRコード.png'
st.image(QR_path)




