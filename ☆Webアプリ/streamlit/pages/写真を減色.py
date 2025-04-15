import streamlit as st
from PIL import Image

# 画像をアップロードするためのファイルアップローダー
uploaded_file = st.file_uploader("アップロードする画像を選んでください。", type=["jpg", "jpeg", "png"])

# 色の数を選択するためのセレクトボックス
num_colors = st.selectbox("減色する色の数を選んでください。", [256, 128, 64])

if uploaded_file is not None:
    # 画像を表示
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption="Original Image", use_column_width=True)

    # 画像を選択された色数に減色する
    quantized_image = original_image.quantize(colors=num_colors)

    # 減色後の画像を表示
    st.image(quantized_image, caption=f"Quantized Image ({num_colors} colors)", use_column_width=True)

    # ダウンロードリンクを提供
    if st.button('Download Quantized Image'):
        # ファイル名を設定
        download_filename = f"quantized_image_{num_colors}_colors.png"
        # ファイルを一時的に保存
        quantized_image.save(download_filename)
        with open(download_filename, "rb") as file:
            st.download_button(label='Click here to download',
                               data=file,
                               file_name=download_filename,
                               mime='image/png')

# サイドバーに情報を表示
st.sidebar.title("About")
st.sidebar.info(
    "これはStreamlitを使用してアップロードされた画像を256色、128色、64色に減色するシンプルなアプリです。"
    "\n\n画像の減色処理にはPILライブラリのquantizeメソッドを使用しています。"
)
