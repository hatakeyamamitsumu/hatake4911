import streamlit as st

# ハイパーリンクを表示するMarkdown文字列
link_str = "[書道ツールです](https://williammer.github.io/works/shodo/)"
# Markdownを表示
st.markdown(link_str, unsafe_allow_html=True)

