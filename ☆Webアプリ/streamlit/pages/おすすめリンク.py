import os
import streamlit as st
st.title("おすすめリンク")
link_str1 = "(https://williammer.github.io/works/shodo/)"
description1 = '↑簡単な書道ができるフリーソフトです。'
st.markdown(f"{link_str1} {description1}", unsafe_allow_html=True)

link_str2 = "(https://gigafile.nu/)"
description2 = '↑ギガファイルサービス。'
st.markdown(f"{link_str2} {description2}", unsafe_allow_html=True)

link_str3 = "(https://qrcode.onl.jp/)"
description3 = '↑QRコードリーダーです。'
st.markdown(f"{link_str3} {description3}", unsafe_allow_html=True)

link_str4 = "(https://1drv.ms/x/c/25c3642a3103cdcb/EcOvbcbbK9ZAqtcuGtxvIKoB0CpKPBG5HYFYx05K9cEVRQ?e=cW1fFT)"
description4 = '↑Hatのプライベートフォルダ。'
st.markdown(f"{link_str4} {description4}", unsafe_allow_html=True)

link_str5 = "(https://1drv.ms/f/c/25c3642a3103cdcb/EleQi7m0oTtBijUzs5uWIJsB37xyltZG6PP6_LzORRJFqQ?e=Guz12t)"
description5 = '↑Hatのプライベートフォルダ。いろんなエクセルファイルが入ったフォルダです。'
st.markdown(f"{link_str5} {description5}", unsafe_allow_html=True)


#st.text('※OneDrive同期（更新）はスタートウインドウから入っておこなうこと。')
st.text('一部スマホではご利用いただけません。')


st.text('')


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
