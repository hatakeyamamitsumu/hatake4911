import os
import streamlit as st
import qrcode
import tempfile

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

# 選択されたリンクのQRコードを生成して保存
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(selected_link[1])
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

# 一時ファイルにQRコードを保存
temp_dir = tempfile.mkdtemp()
temp_file_path = os.path.join(temp_dir, "qr_code.png")
img.save(temp_file_path)

# Streamlitに画像を表示
st.image(temp_file_path, caption="QRコード", use_column_width=True)
