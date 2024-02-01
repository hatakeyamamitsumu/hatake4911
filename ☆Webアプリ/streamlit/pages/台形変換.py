import streamlit as st
import cv2
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
        # Load the image
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)

        # Initialize destination points with default values
        default_values = [0.25, 0.2, 0.75, 0.1, 1.0, 0.5, 0.0, 0.8]
        dst_pts = np.array([[image.shape[1] * default_values[i], image.shape[0] * default_values[i + 1]] for i in range(0, len(default_values), 2)], dtype=np.float32)

        # Allow users to interactively adjust destination points
        st.subheader("Adjust Destination Points:")
        for i in range(4):
            row = st.slider(f"Point {i + 1} X", 0.0, 1.0, default_values[i * 2], 0.01)
            col = st.slider(f"Point {i + 1} Y", 0.0, 1.0, default_values[i * 2 + 1], 0.01)
            dst_pts[i] = [row * image.shape[1], col * image.shape[0]]

        # Apply perspective transformation
        result = perspective_transform(image, dst_pts)

        # Display original and transformed images with the same color space
        st.image(image, caption='Original Image', use_column_width=True, channels="BGR")
        st.image(result, caption='Perspective Transformed Image', use_column_width=True, channels="BGR")

        # Save transformed image with the same color space
        st.download_button(
            label="Download Transformed Image",
            data=cv2.imencode('.jpg', result)[1].tobytes(),
            file_name='Perspective_Transformed_Image.jpg',
            mime='image/jpg'
        )

if __name__ == '__main__':
    main()
