import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def main():
    st.title("標識（？）作成アプリ")
    st.write("当初は標識を作成するアプリを作る予定でしたが、大幅に脱線しました・・・・。")
    st.write("写真をアップロードして、4番目の層に重ねてください。")

    # アップロードされた画像
    uploaded_image = st.file_uploader("写真をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        ImgObj = Image.open(uploaded_image)
        ImgObj = ImgObj.convert('RGBA') if ImgObj.mode == "RGB" else ImgObj  # JPEGをRGBAに変換

        # 4番目の層の画像を取得
        fourth_layer_image_path = os.path.join("/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第四層", 
                                             random.choice(os.listdir("/mount/src/hatake4911/☆Webアプリ/画像/標識用画像/第四層")))
        fourth_layer_image = Image.open(fourth_layer_image_path)

        # 画像サイズを合わせる
        width_ratio = fourth_layer_image.size[0] / ImgObj.size[0]
        height_ratio = fourth_layer_image.size[1] / ImgObj.size[1]
        resize_ratio = min(width_ratio, height_ratio)
        new_size = (int(ImgObj.size[0] * resize_ratio), int(ImgObj.size[1] * resize_ratio))
        ImgObj = ImgObj.resize(new_size, Image.ANTIALIAS)

        # 画像を重ねる
        wmCanvas = Image.new('RGBA', fourth_layer_image.size, (255, 255, 255, 0))  # 透かし画像の生成
        wmCanvas.paste(fourth_layer_image, (0, 0), fourth_layer_image)
        wmCanvas.paste(ImgObj, (0, 0), ImgObj)  # 透かし画像を貼り付け

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
