import streamlit as st
from PIL import Image
from openpyxl import Workbook
from openpyxl.styles import PatternFill
import io

def image_to_excel(image, output_filename):
    # 画像の幅と高さを取得
    width, height = image.size

    # 新しいExcelブックを作成
    workbook = Workbook()
    sheet = workbook.active

    # 画像の各ピクセルをExcelセルに対応させて色を設定
    for y in range(height):
        for x in range(width):
            pixel_color = image.getpixel((x, y))
            hex_color = f'{pixel_color[0]:02X}{pixel_color[1]:02X}{pixel_color[2]:02X}'  # RGBを16進数に変換
            fill = PatternFill(start_color=hex_color, end_color=hex_color, fill_type='solid')
            cell = sheet.cell(row=y + 1, column=x + 1)
            cell.fill = fill

    # Excelファイルを保存
    workbook.save(output_filename)
    return output_filename

def main():
    st.title("Image to Excel Color Converter")

    # 画像ファイルをアップロード
    image_file = st.file_uploader("Upload Image File", type=["jpg", "jpeg", "png"])

    if image_file is not None:
        # 画像をPIL形式に変換
        image = Image.open(image_file)

        # 画像を表示
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # 出力ファイル名を指定
        output_excel_filename = st.text_input("Output Excel Filename", "output_colors.xlsx")

        # 変換ボタン
        if st.button("Convert and Save to Excel"):
            output_filename = image_to_excel(image, output_excel_filename)
            st.success(f'Image colors saved in Excel: {output_filename}')

            # ダウンロードボタン
            download_button = st.download_button(
                label="Download Excel File",
                data=io.BytesIO(),
                file_name=output_filename,
                key="download_button",
            )

if __name__ == "__main__":
    main()
