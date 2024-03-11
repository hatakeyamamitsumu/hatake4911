import os
import streamlit as st

# リンクと説明のリスト。
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

selected_index = st.selectbox("表示したいリンク番号を選択してください", range(len(links)))


# 選択されたリンクと説明を表示
selected_link, selected_description = links[selected_index]
st.markdown(f"{selected_link} {selected_description}", unsafe_allow_html=True)


# 画像ファイルが保存されているフォルダのパス
image_folder_path = "/mount/src/hatake4911/☆Webアプリ/QRコード各種"

# フォルダ内の画像ファイルのリストを取得
image_files = [f for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# 画像ファイルを選択するセレクトボックスを表示
selected_image = st.selectbox("QRコード用意してます。リストから選択してください", image_files)

# 選択された画像ファイルのパスを作成
selected_image_path = os.path.join(image_folder_path, selected_image)
st.image(selected_image_path, caption=f"選択された画像ファイル: {selected_image}")

