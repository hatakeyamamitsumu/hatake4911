import os
import streamlit as st

# リンクと説明のリスト
links = [
    ("https://williammer.github.io/works/shodo/", "←　簡単な書道ができるフリーソフトです。"),
    ("https://gigafile.nu/", "←　ギガファイルサービス。"),
    ("https://qrcode.onl.jp/", "←　QRコードリーダーです。"),
    ("https://1drv.ms/f/c/25c3642a3103cdcb/EtW74Af8pZJEvbgsxfhCAgoBBufG7sLiDQJKDcu2UhWzNw?e=6KTvOs", "←　Hatの画像フォルダ。"),
    ("https://1drv.ms/f/c/25c3642a3103cdcb/EleQi7m0oTtBijUzs5uWIJsB37xyltZG6PP6_LzORRJFqQ?e=Guz12t", "←　Hatのプライベートフォルダ。いろんなエクセルファイルが入ったフォルダです。"),
]

# タイトル
st.title("おすすめリンク")

# 選択ボックス
selected_index = st.selectbox("表示したいリンクを選択してください", range(len(links)))

# 選択されたリンクと説明を表示
selected_link, selected_description = links[selected_index]
st.markdown(f"{selected_link} {selected_description}", unsafe_allow_html=True)
