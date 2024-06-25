import streamlit as st
from PIL import Image

# 画像をアップロードするためのファイルアップローダー
uploaded_file = st.file_uploader("アップロードする画像を選んでください。", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を表示
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption="Original Image", use_column_width=True)

    # 画像を256色に減色する
    quantized_image = original_image.quantize(colors=256)

    # 減色後の画像を表示
    st.image(quantized_image, caption="Quantized Image (256 colors)", use_column_width=True)

    # ダウンロードリンクを提供
    if st.button('Download Quantized Image'):
        # ファイル名を設定
        download_filename = "quantized_image_256_colors.png"
        # ファイルをダウンロード
        quantized_image.save(download_filename)
        st.download_button(label='Click here to download',
                           data=download_filename,
                           file_name=download_filename,
                           mime='image/png')

# サイドバーに情報を表示
st.sidebar.title("About")
st.sidebar.info(
    "これはStreamlitを使用してアップロードされた画像を256色に減色するシンプルなアプリです。"
    "\n\n画像の減色処理にはPILライブラリのquantizeメソッドを使用しています。"
)
