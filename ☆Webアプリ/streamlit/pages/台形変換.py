import streamlit as st
import cv2
import matplotlib.pyplot as plt
import numpy as np

def perspective_transform(img, dst_pts):
    src_pts = np.array([[0, 0], [img.shape[1], 0], [img.shape[1], img.shape[0]], [0, img.shape[0]]], dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    result = cv2.warpPerspective(img, matrix, (img.shape[1], img.shape[0]))
    return result

def main():
    st.title("Perspective Transformation App")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)

        # Display uploaded image
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption='Original Image', use_column_width=True)

        # Allow user to input destination points
        st.subheader("Adjust Destination Points:")
        dst_pts = []
        for i in range(4):
            row = st.slider(f"Point {i + 1}", 0.0, float(image.shape[1]), float(image.shape[1] * 0.5))
            col = st.slider(f"    ", 0.0, float(image.shape[0]), float(image.shape[0] * 0.5))
            dst_pts.append([row, col])
        
        dst_pts = np.array(dst_pts, dtype=np.float32)

        # Apply perspective transformation
        result = perspective_transform(image, dst_pts)

        # Display transformed image
        st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), caption='Perspective Transformed Image', use_column_width=True)

        # Save transformed image
        st.download_button(label="Download Transformed Image", data=cv2.imencode('.jpg', cv2.cvtColor(result, cv2.COLOR_BGR2RGB))[1].tobytes(), file_name='Perspective_Transformed_Image.jpg', mime='image/jpg')

if __name__ == '__main__':
    main()
