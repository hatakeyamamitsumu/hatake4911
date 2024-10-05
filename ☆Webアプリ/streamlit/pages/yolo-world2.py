import streamlit as st
from ultralytics import YOLOWorld
import cv2

# YOLO-World model loading (replace with your model path)
model = YOLOWorld('yolov8s.pt')

def detect_objects(uploaded_image):
  """
  Function to handle image upload, processing, and error handling.

  Args:
      uploaded_image (streamlit.UploadedFile): User uploaded image file.

  Returns:
      None: If an error occurs, displays an error message to the user.
              Otherwise, displays the processed image with detections.
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
      annotated_img = results[0].plot(cmap='hsv')  # Display detections with colormap

      # Display processed image with detections
      st.image(annotated_img, channels="BGR", use_column_width=True)

    except Exception as e:
      st.error(f"Error processing image: {e}")

# Streamlit app layout
st.title("YOLOv8 Object Detection with Streamlit")
st.subheader("Upload an image file (JPG or PNG only)")
uploaded_image = st.file_uploader("", type=['jpg', 'png'])

# Call the detection function
detect_objects(uploaded_image)
