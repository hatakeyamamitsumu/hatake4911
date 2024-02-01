import streamlit as st
import cv2
import numpy as np

def perspective_transform(img, dst_pts):
    src_pts = np.array([[0, 0], [img.shape[1], 0], [img.shape[1], img.shape[0]], [0, img.shape[0]]], dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    result = cv2.warpPerspective(img, matrix, (img.shape[1], img.shape[0]))
    return result

def main():
    st.title("画像をひし形に歪めるアプリ")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load the image
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)

        # Initialize destination points with default values
        default_values = [0.25, 0.2, 0.75, 0.1, 1.0, 0.5, 0.0, 0.8]
        dst_pts = np.array([[image.shape[1] * default_values[i], image.shape[0] * default_values[i + 1]] for i in range(0, len(default_values), 2)], dtype=np.float32)

        # Allow users to interactively adjust destination points
        st.subheader("Adjust Destination Points:")
        st.text("デフォルト値は1X=0.00,1Y=0.00,2X=1.00,2Y=0.00,3X=1.00,3Y=1.00,4X=0.00,4Y=1.00です。")
        for i in range(4):
            row = st.slider(f"Point {i + 1} X", 0.0, 1.0, default_values[i * 2], 0.01)
            col = st.slider(f"Point {i + 1} Y", 0.0, 1.0, default_values[i * 2 + 1], 0.01)
            dst_pts[i] = [row * image.shape[1], col * image.shape[0]]

        # Apply perspective transformation
        result = perspective_transform(image, dst_pts)

        # Display original and transformed images
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption='Original Image', use_column_width=True)
        st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), caption='Perspective Transformed Image', use_column_width=True)

        # Save transformed image
        st.download_button(label="Download Transformed Image", data=cv2.imencode('.jpg', cv2.cvtColor(result, cv2.COLOR_BGR2RGB))[1].tobytes(), file_name='Perspective_Transformed_Image.jpg', mime='image/jpg')

if __name__ == '__main__':
    main()
