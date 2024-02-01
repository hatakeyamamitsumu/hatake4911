import streamlit as st
st.title("おすすめリンク")
st.text('一部スマホではご利用いただけません。')
# ハイパーリンクを表示するMarkdown文字列
link_str = "[The Shodo](https://williammer.github.io/works/shodo/)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('簡単な書道ができるフリーソフトです。')

# ハイパーリンクを表示するMarkdown文字列
link_str = "[QRコード読み取り](https://qrcode.onl.jp/)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('QRコードリーダーです。')

# ハイパーリンクを表示するMarkdown文字列
link_str = "[自分のエクセルブック](https://1drv.ms/x/c/25c3642a3103cdcb/Ecn7kcD0QC1EqpBxqe0ZpgEBNSiFlTUkDm0G1uj8S3mzFw?e=Zthahb)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('自分のエクセルブックです。')

# ハイパーリンクを表示するMarkdown文字列
link_str = "(https://1drv.ms/f/c/25c3642a3103cdcb/EtW74Af8pZJEvbgsxfhCAgoBBufG7sLiDQJKDcu2UhWzNw?e=8ts0p1)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('画像フォルダです')


