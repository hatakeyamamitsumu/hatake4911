import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def main():
    st.title("標識（？）作成アプリ")
    st.write("当初は標識を作成するアプリを作る予定でしたが、大幅に脱線しました・・・・。")
    st.write("それぞれのリストからお好みの絵を選択して重ねてください。")

    # 画像フォルダのパス
    image_folders = [
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第一層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第二層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第三層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第四層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第五層",
        "/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第六層",
    ]

    # アップロードされた画像
    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        uploaded_img = Image.open(uploaded_image)
        uploaded_img = uploaded_img.convert('RGBA') if uploaded_img.mode == "RGB" else uploaded_img  # JPEGをRGBAに変換

    # 画像ファイルの選択
    selected_images = []
    for folder in image_folders:
        image_files = os.listdir(folder)
        selected_image = st.selectbox("", [os.path.join(folder, image_file) for image_file in image_files], index=0)
        selected_images.append(Image.open(selected_image))

    # アップロードされた画像と他の画像のサイズを合わせる
    max_width = max(img.size[0] for img in selected_images) if selected_images else 0
    max_height = max(img.size[1] for img in selected_images) if selected_images else 0

    if uploaded_image is not None:
        uploaded_width, uploaded_height = uploaded_img.size
        uploaded_ratio = max(max_width / uploaded_width, max_height / uploaded_height)
        new_uploaded_size = (int(uploaded_width * uploaded_ratio), int(uploaded_height * uploaded_ratio))
        uploaded_img = uploaded_img.resize(new_uploaded_size, Image.ANTIALIAS)
        selected_images.append(uploaded_img)

    wmCanvas = Image.new('RGBA', (max_width, max_height), (255, 255, 255, 0))  # 透かし画像の生成
    y_offset = 0
    for img in selected_images:
        offset_x = (max_width - img.size[0]) // 2
        wmCanvas.paste(img, (offset_x, y_offset), img)  # 透かし画像を貼り付け
        y_offset += img.size[1]

    WMedImage = wmCanvas  # 画像の合成

    # 画像を表示
    st.image(WMedImage, caption='合成された画像')

    # 画像をダウンロードするボタン
    def download_image(image, filename='合成された画像.png'):
        image.save(filename, 'PNG')
        with open(filename, 'rb') as f:
            data = f.read()
        return data

    if st.button("ダウンロードしますか？"):
        data = download_image(WMedImage)
        st.download_button(
            label="ここをクリックしてダウンロード",
            data=data,
            file_name='合成された画像.png',
            mime='image/png'
        )

if __name__ == '__main__':
    main()
