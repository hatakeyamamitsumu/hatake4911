import os
import streamlit as st

# リンクと説明のリスト。
links = [
    ( "簡単な書道ができるフリーソフトです。","https://williammer.github.io/works/shodo/"),
    ( "ギガファイルサービス。","https://gigafile.nu/"),
    ( "QRコードリーダーです。","https://qrcode.onl.jp/"),
    ( "Hatの画像フォルダ。","https://1drv.ms/f/c/25c3642a3103cdcb/EtW74Af8pZJEvbgsxfhCAgoBBufG7sLiDQJKDcu2UhWzNw?e=6KTvOs"),
    ( "Hatのプライベートフォルダ。いろんなエクセルファイルが入ったフォルダです。","https://1drv.ms/f/c/25c3642a3103cdcb/EleQi7m0oTtBijUzs5uWIJsB37xyltZG6PP6_LzORRJFqQ?e=Guz12t"),
]

# タイトル
st.title("おすすめリンク")

# 選択ボックス

selected_link = st.selectbox("表示したいリンクを選択してください", links)

# 選択されたリンクと説明を表示
st.markdown(f"""
- **リンク:** {selected_link[0]}
- **説明:** {selected_link[1]}
""", unsafe_allow_html=True)

# 画像ファイルが保存されているフォルダのパス
image_folder_path = "/mount/src/hatake4911/☆Webアプリ/QRコード各種"

# フォルダ内の画像ファイルのリストを取得
image_files = [f for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# 画像ファイルを選択するセレクトボックスを表示
selected_image = st.selectbox("QRコード用意してます。リストから選択してください", image_files)

# 選択された画像ファイルのパスを作成
selected_image_path = os.path.join(image_folder_path, selected_image)

# 選択された画像ファイルを表示
st.image(selected_image_path, caption=f"選択された画像ファイル: {selected_image}")
