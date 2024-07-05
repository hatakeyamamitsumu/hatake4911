import cv2
import pytesseract
from PIL import Image

# 画像ファイルのパス
image_path = 'path_to_your_image.jpg'

# 画像を読み込む
image = cv2.imread(image_path)

# 画像をグレースケールに変換
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ノイズ除去
gray = cv2.medianBlur(gray, 3)

# 画像を二値化
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# TesseractでOCRを実行
text = pytesseract.image_to_string(binary, lang='eng')

print("抽出されたテキスト:")
print(text)

# 結果を保存したい場合は、以下のコードを追加
output_path = 'output_text.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"抽出されたテキストを {output_path} に保存しました。")
