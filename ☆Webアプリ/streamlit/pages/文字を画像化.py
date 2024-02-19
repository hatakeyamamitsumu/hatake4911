from PIL import Image, ImageDraw, ImageFont

def text_to_image(text, output_path):
    # 画像サイズと背景色を設定
    width, height = 100, 100  # 任意のサイズ
    background_color = "white"

    # 画像を作成
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 使用するフォントとテキストの設定
    font_size = 20
    font = ImageFont.truetype("/mount/src/hatake4911/☆Webアプリ/フォントファイル/HGRPRE.TTC", font_size)  # フォントは適切なものを指定
    text_color = "black"

    # テキストを中央に配置
    text_width, text_height = draw.textsize(text, font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # テキストを描画
    draw.text((x, y), text, font=font, fill=text_color)

    # 画像を保存
    image.save(output_path)

# 使用例
text_to_image("山", "mountain.jpg")
