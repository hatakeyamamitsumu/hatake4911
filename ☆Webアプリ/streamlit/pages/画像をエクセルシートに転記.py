import streamlit as st
from PIL import Image
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import PatternFill

def image_to_excel(image_stream, output_filename):
    # 画像ファイルを開く
    image = Image.open(image_stream)

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

# Streamlit UI
st.title("Image to Excel Converter")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Convert image to Excel when button is clicked
    if st.button("Convert to Excel"):
        # Set the output file name
        output_excel_filename = "画像をエクセル化.xlsx"
        
        # Call the conversion function with the BytesIO object
        result_filename = image_to_excel(uploaded_file, output_excel_filename)

        # Display download link for the Excel file
        st.success(f"Image colors saved in Excel: {result_filename}")
        st.download_button(
            label="Download Excel File",
            data=result_filename,
            key="download_button",
            on_click=None,
            args=None,
            help="Click to download the Excel file.",
        )
