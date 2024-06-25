import streamlit as st
from PIL import Image, ImageOps

# 画像をアップロードするためのファイルアップローダー
uploaded_file = st.file_uploader("アップロードする画像を選んでください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を表示
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption="Original Image", use_column_width=True)

    # 減色の深さを選択
    num_colors = st.slider("減色の深さを選択してください", min_value=2, max_value=256, value=16, step=1)

    # 画像の減色処理
    with st.spinner('処理中...'):
        quantized_image = ImageOps.posterize(original_image, num_colors)

    st.success("処理が完了しました！")

    # 減色後の画像を表示
    st.image(quantized_image, caption=f"Quantized Image (Colors: {num_colors})", use_column_width=True)

    # ダウンロードリンクを提供
    if st.button('Download Quantized Image'):
        # ファイル名を設定
        download_filename = f"quantized_image_{num_colors}_colors.png"
        # ファイルをダウンロード
        quantized_image.save(download_filename)
        st.download_button(label='Click here to download',
                           data=download_filename,
                           file_name=download_filename,
                           mime='image/png')

# サイドバーに情報を表示
st.sidebar.title("About")
st.sidebar.info(
    "これはStreamlitを使用してアップロードされた画像を減色するシンプルなアプリです。"
    "\n\n減色処理には色の量子化（Posterize）を使用しています。"
)
