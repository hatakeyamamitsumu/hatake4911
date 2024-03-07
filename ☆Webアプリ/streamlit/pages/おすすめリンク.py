import streamlit as st

def display_link(link, description):
    st.markdown(link, unsafe_allow_html=True)
    st.text(description)

st.title("おすすめリンク")
st.text('一部スマホではご利用いただけません。')

# リンクと説明文を表示
link = "(https://williammer.github.io/works/shodo/)"
description = '↑簡単な書道ができるフリーソフトです。'
display_link(link, description)

link = "(https://gigafile.nu/)"
description = '↑ギガファイルサービス'
display_link(link, description)

link = "(https://qrcode.onl.jp/)"
description = '↑QRコードリーダーです。'
display_link(link, description)

link = "(https://1drv.ms/x/c/25c3642a3103cdcb/EcOvbcbbK9ZAqtcuGtxvIKoB0CpKPBG5HYFYx05K9cEVRQ?e=cW1fFT)"
description = '↑Hatのプライベートフォルダ。マクロ等の挙動テスト用エクセルブック'
display_link(link, description)

link = "(https://1drv.ms/f/c/25c3642a3103cdcb/EtW74Af8pZJEvbgsxfhCAgoBBufG7sLiDQJKDcu2UhWzNw?e=dy53br)"
description = '↑Hatのプライベートフォルダ。画像フォルダです'
display_link(link, description)



# 画像ファイルが保存されているフォルダのパス
image_folder_path = "/mount/src/hatake4911/☆Webアプリ/QRコード各種"

# フォルダ内の画像ファイルのリストを取得
image_files = [f for f in os.listdir(image_folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# 画像ファイルを選択するセレクトボックスを表示
selected_image = st.selectbox("画像ファイルを選択してください", image_files)

# 選択された画像ファイルのパスを作成
selected_image_path = os.path.join(image_folder_path, selected_image)

# 選択された画像を表示
st.image(selected_image_path, caption=f"選択された画像ファイル: {selected_image}")

# 選択された画像ファイルのファイル名を表示
st.write(f"選択された画像ファイルのファイル名: {selected_image}")
