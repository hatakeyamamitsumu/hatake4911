import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
from rembg import remove
from io import BytesIO

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
  uploaded_image = st.file_uploader("写真をアップロードしてください", type=["jpg", "jpeg", "png"])

  # 画像処理
  uploaded_images = process_uploaded_image(uploaded_image)

  # 画像ファイルの選択
  for folder in image_folders:
    image_files = os.listdir(folder)
    selected_image = st.selectbox("", image_files, index=0)
    uploaded_images.append(center_align(Image.open(os.path.join(folder, selected_image))))

  # 画像の合成
  WMedImage = composite_images(uploaded_images)

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

# 画像処理関数
def process_uploaded_image(image):
  if image is None:
    return []

  # 背景を切り抜く
  if st.checkbox("背景を切り抜く"):
    image = remove_background(image)

  # 画像を中央揃えにする
  image = center_align(image)

  return [image]

# 背景切り抜き関数
def remove_background(image):
  image_bytes = image.read()
  img = Image.open(BytesIO(image_bytes))
  img = remove(img)
  return img

# 画像の中央揃え関数
def center_align(img):
  width, height = img.size
  new_img = Image.new("RGBA", (max(width, height), max(width, height)), (255, 255, 255, 0))
  position = ((max(width, height) - width) // 2, (max(width, height) - height) // 2)
  new_img.paste(img, position)
  return new_img

# 画像の合成関数
def composite_images(images):
  max_width = max(img.size[0] for img in images)
  max_height = max(img.size[1] for img in images)
  wmCanvas = Image.new('RGBA', (max_width, max_height), (255, 255, 255, 0)) # 透かし画像の生成
  for i, img in enumerate(images):
    wmCanvas.paste(img, (0, 0), img) # 透かし画像を貼り付け

  return wmCanvas

if __name__ == '__main__':
  main()
