import streamlit as st
st.title("おすすめリンク")
st.text('※OneDrive同期はスタートウインドウから入っておこなうこと。')
st.text('一部スマホではご利用いただけません。')
# ハイパーリンクを表示するMarkdown文字列
link_str = "(https://williammer.github.io/works/shodo/)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('↑簡単な書道ができるフリーソフトです。')

# ハイパーリンクを表示するMarkdown文字列
link_str = "(https://qrcode.onl.jp/)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('↑QRコードリーダーです。')

# ハイパーリンクを表示するMarkdown文字列
link_str = "(https://1drv.ms/x/c/25c3642a3103cdcb/EcOvbcbbK9ZAqtcuGtxvIKoB0CpKPBG5HYFYx05K9cEVRQ?e=cW1fFT)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('↑マクロ等の挙動テスト用エクセルブック')

# ハイパーリンクを表示するMarkdown文字列
link_str = "(https://1drv.ms/f/c/25c3642a3103cdcb/EtW74Af8pZJEvbgsxfhCAgoBBufG7sLiDQJKDcu2UhWzNw?e=dy53br)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('↑画像フォルダです')


# ハイパーリンクを表示するMarkdown文字列
link_str = "(https://1drv.ms/f/c/25c3642a3103cdcb/EleQi7m0oTtBijUzs5uWIJsB37xyltZG6PP6_LzORRJFqQ?e=Guz12t)"
# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
st.text('↑いろんなエクセルファイルが入ったフォルダです。')
