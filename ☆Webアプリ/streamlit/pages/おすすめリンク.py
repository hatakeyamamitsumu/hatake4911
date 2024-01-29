import streamlit as st

# ハイパーリンクを表示するMarkdown文字列
link_str = "[The Shodo](https://williammer.github.io/works/shodo/)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('簡単な書道ができるフリーソフトです。')

# ハイパーリンクを表示するMarkdown文字列
link_str = "[The Shodo](https://qrcode.onl.jp/)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('QRコードリーダーです。')
