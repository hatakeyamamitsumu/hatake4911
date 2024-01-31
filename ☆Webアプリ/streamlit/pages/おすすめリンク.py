import streamlit as st

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
https://1drv.ms/x/c/25c3642a3103cdcb/Ecn7kcD0QC1EqpBxqe0ZpgEBNSiFlTUkDm0G1uj8S3mzFw?e=Zthahb
# ハイパーリンクを表示するMarkdown文字列
link_str = "[自分のエクセルブック](https://1drv.ms/x/c/25c3642a3103cdcb/Ecn7kcD0QC1EqpBxqe0ZpgEBNSiFlTUkDm0G1uj8S3mzFw?e=Zthahb)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('自分のエクセルブックです。')
