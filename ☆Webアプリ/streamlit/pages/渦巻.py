# オリジナル画像と渦巻き後の画像のダウンロードボタン
st.download_button(
    label="オリジナル画像をダウンロード",
    data=uploaded_file.getvalue(),
    file_name="original_image.png",
)

# 渦巻き後の画像をバイトに変換
processed_image_bytes = processed_image_with_bg.convert("RGB").tobytes()

st.download_button(
    label="渦巻き後の画像をダウンロード",
    data=processed_image_bytes,
    file_name="swirled_image.png",
)
