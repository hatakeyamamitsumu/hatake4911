import streamlit as st
from PIL import Image
import pytesseract

st.title("OCR App using Streamlit and Tesseract")

st.write("Upload an image and the app will extract text from it using OCR.")

uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    st.write("Extracting text...")
    
    # Use pytesseract to do OCR on the image
    extracted_text = pytesseract.image_to_string(image)
    
    # Display the extracted text
    st.write("Extracted Text:")
    st.write(extracted_text)
