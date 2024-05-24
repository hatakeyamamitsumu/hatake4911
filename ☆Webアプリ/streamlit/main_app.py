import streamlit as st
from PIL import Image
import os
import random
import io
import qrcode

st.title('Hatの、WEBアプリ作り挑戦日記')
st.write('こんにちは！Hatと申します。')

st.subheader('自己紹介')
st.write('プログラミングは初心者ですが、簡易なWEBアプリ「streamlit」を使って何かできないかと考えて、発表し続けようと考えております。\nよろしくお願いします。')
st.text('オリジナルでないコードも含まれますが、可能な限り出典を明示させていただきます。')
st.text("")
# ハイパーリンクを表示するMarkdown文字列

# Markdownを表示。
st.markdown(link_str, unsafe_allow_html=True)
link_str = "(https://forms.gle/DUHCTT5CfajGjoGMA)"
st.write('感想をお聞かせください。')
st.text('無記名アンケートです。差し支えなければお答えください。')

QR_path='/mount/src/hatake4911/☆Webアプリ/QRコード各種/アンケートフォーム用QR.png'
st.image(QR_path, width=150)






# リンクと説明のリスト
links = [
    ("簡単な書道ができるフリーソフトです。", "https://williammer.github.io/works/shodo/"),
    ("ギガファイルサービス。", "https://gigafile.nu/"),
    ("QRコードリーダーです。", "https://qrcode.onl.jp/"),
    ("Hatの画像フォルダ。", "https://1drv.ms/f/c/25c3642a3103cdcb/EtW74Af8pZJEvbgsxfhCAgoBBufG7sLiDQJKDcu2UhWzNw?e=6KTvOs"),
    ("Hatのプライベートフォルダ。いろんなエクセルファイルが入ったフォルダです。", "https://1drv.ms/f/c/25c3642a3103cdcb/EleQi7m0oTtBijUzs5uWIJsB37xyltZG6PP6_LzORRJFqQ?e=Guz12t"),
]

# タイトル
st.title("おすすめリンク")

# 選択ボックス
selected_link = st.selectbox("表示したいリンクを選択してください", links)

# 選択されたリンクと説明を表示
st.markdown(f"""**リンク:** {selected_link[1]}""", unsafe_allow_html=True)

# 選択されたリンクのQRコードを生成してバイトデータとして取得
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(selected_link[1])
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

# PILイメージをバイトデータに変換
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='PNG')
img_byte_arr = img_byte_arr.getvalue()

# Streamlitにバイトデータを表示　, use_column_width=True
st.image(img_byte_arr, caption="QRコード")

