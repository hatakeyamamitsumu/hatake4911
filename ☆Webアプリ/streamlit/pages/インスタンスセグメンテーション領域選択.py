import streamlit as st
import cv2
import numpy as np
import torch
import torchvision
from torchvision import transforms as T
from PIL import Image

# Load a pre-trained model for instance segmentation
@st.cache(allow_output_mutation=True)
def load_model():
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    return model

model = load_model()

# Function to apply the instance segmentation model
def get_segmentation_masks(image, model, threshold=0.5):
    transform = T.Compose([T.ToTensor()])
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image)
    scores = outputs[0]['scores'].numpy()
    masks = outputs[0]['masks'].numpy()
    labels = outputs[0]['labels'].numpy()
    return masks[scores > threshold], labels[scores > threshold]

# Streamlit interface
st.title("Instance Segmentation Blurring App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    masks, labels = get_segmentation_masks(image, model)
    
    # Convert PIL image to OpenCV format
    cv_image = np.array(image)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    
    checkbox_vars = []
    st.write("Select the instances you want to blur:")
    for i, label in enumerate(labels):
        var = st.checkbox(f"Instance {i+1} (Label {label})")
        checkbox_vars.append(var)

    if st.button("Apply Blur"):
        blurred_image = cv_image.copy()
        for i, var in enumerate(checkbox_vars):
            if var:
                mask = masks[i, 0]
                mask = cv2.resize(mask, (cv_image.shape[1], cv_image.shape[0]))
                mask = (mask > 0.5).astype(np.uint8)
                blurred_image = cv2.blur(blurred_image, (15, 15), dst=blurred_image, mask=mask)
        st.image(cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB), caption='Blurred Image', use_column_width=True)
