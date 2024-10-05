import streamlit as st
from ultralytics import YOLOWorld
import cv2
import numpy as np


def detect_objects(uploaded_image):
  """
  Function to handle image upload, processing, and error handling.

  Args:
      uploaded_image (streamlit.UploadedFile): User uploaded image file.

  Returns:
      cv2.Mat: The processed image with detections (BGR format).
      None: If an error occurs.
  """
  if uploaded_image is not None:
    try:
      # Access uploaded image using its name
      img = cv2.imdecode(np.frombuffer(uploaded_image.getvalue(), np.uint8), cv2.IMREAD_COLOR)

      # Check if image decoding was successful
      if img is None:
        raise Exception("Failed to decode uploaded image.")

      # Object detection using YOLOv8
      results = model.predict(source=img)
      annotated_img = results[0].plot(cmap='hsv')  # Display detections with colormap (BGR format)

      return annotated_img

    except Exception as e:
      st.error(f"Error processing image: {e}")
      return None  # Indicate error

  return None  # No image uploaded


def display_results(processed_image):
  """
  Function to display the processed image with detections in Streamlit.

  Args:
      processed_image (cv2.Mat): The processed image with detections (BGR format).
  """
  if processed_image is not None:
    # Convert BGR to RGB for Streamlit display
    rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
    st.image(rgb_image, channels="RGB", use_column_width=True)


# Streamlit app layout
st.title("YOLOv8 Object Detection with Streamlit")
st.subheader("Upload an image file (JPG or PNG only)")
uploaded_image = st.file_uploader("", type=['jpg', 'png'])

# Call the detection function
processed_image = detect_objects(uploaded_image)

# Display the results if processing was successful
display_results(processed_image)
