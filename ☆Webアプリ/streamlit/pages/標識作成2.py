import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

def center_align(img):
    width, height = img.size
    new_img = Image.new("RGBA", (max(width, height), max(width, height)), (255, 255, 255, 0))
    position = ((max(width, height) - width) // 2, (max(width, height) - height) // 2)
    new_img.paste(img, position)
    return new_img

def main():
    st.title("標識（？）作成アプリ")
    st.write("当初は標識を作成するアプリを作る予定でしたが、大幅に脱線しました・・・・。")
    st.write("それぞれのリストからお好みの絵を選択して重ねてください。")
    st.write("写真をアップロードする場合は、一番上のリストは「なし」を選択してください。")
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
    uploaded_image1 = st.file_uploader("1つ目の写真をアップロードしてください", type=["jpg", "jpeg", "png"])
    uploaded_image2 = st.file_uploader("2つ目の写真をアップロードしてください", type=["jpg", "jpeg", "png"])

    if uploaded_image1 is not None:
        ImgObj1 = Image.open(uploaded_image1)
        ImgObj1 = ImgObj1.convert('RGBA') if ImgObj1.mode == "RGB" else ImgObj1  # JPEGをRGBAに変換
        uploaded_images = [center_align(ImgObj1)]

    else:
        uploaded_images = []

    # 2つ目のアップローダーも同じように処理
    if uploaded_image2 is not None:
        ImgObj2 = Image.open(uploaded_image2)
        ImgObj2 = ImgObj2.convert('RGBA') if ImgObj2.mode == "RGB" else ImgObj2  # JPEGをRGBAに変換
        uploaded_images.append(center_align(ImgObj2))

    else:
        uploaded_images.append(None)

    # 画像ファイルの選択
    for folder in image_folders:
        image_files = os.listdir(folder)
        selected_image = st.selectbox("", image_files, index=0)
        uploaded_images.append(center_align(Image.open(os.path.join(folder, selected_image))))

    # 4番目の画像を最前面に配置
    uploaded_images[3], uploaded_images[0] = uploaded_images[0], uploaded_images[3]

    # None を除いた画像のリストを取得
    filtered_images = [img for img in uploaded_images if img is not None]

    if not filtered_images:
        st.error("Please upload at least one image.")
        return

    # 最大幅と最大高さを取得
    max_width = max(img.size[0] for img in filtered_images)
    max_height = max(img.size[1] for img in filtered_images)

    # 画像のサイズに合わせて縮小拡大
    for i, img in enumerate(uploaded_images):
        width_ratio = max_width / img.size[0]
        height_ratio = max_height / img.size[1]
        resize_ratio = min(width_ratio, height_ratio)
        new_size = (int(img.size[0] * resize_ratio), int(img.size[1] * resize_ratio))
        uploaded_images[i] = img.resize(new_size, Image.ANTIALIAS)
    ImgObjs = uploaded_images

    wmCanvas = Image.new('RGBA', (max_width, max_height), (255, 255, 255, 0))  # 透かし画像の生成
    for i, img in enumerate(ImgObjs):
        if img is not None:
            wmCanvas.paste(img, (0, 0), img)  # 透かし画像を貼り付け

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
