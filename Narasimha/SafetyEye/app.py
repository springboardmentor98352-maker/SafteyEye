import streamlit as st
from utils.data_loader import load_data
from utils.trainer import train_model
from utils.detector import detect_ppe
import pandas as pd

# Set up the Streamlit app
st.title("SafetyEye - AI-Powered Workplace Occupancy & Safety Monitor")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a page:", ["Data Preparation", "Model Training", "Live Detection", "Dashboard"])

if options == "Data Preparation":
    st.header("Data Preparation")
    if st.button("Download Dataset"):
        load_data()
        st.success("Dataset downloaded and processed successfully!")
    else:
        st.info("Click the button to download the dataset.")

elif options == "Model Training":
    st.header("Model Training")
    model_size = st.selectbox("Select Model Size:", ["nano", "small", "medium"])
    epochs = st.number_input("Epochs:", min_value=1, max_value=500, value=50)
    batch_size = st.number_input("Batch Size:", min_value=1, value=16)
    
    if st.button("Start Training"):
        train_model(model_size, epochs, batch_size)
        st.success("Model training started!")

elif options == "Live Detection":
    st.header("Live Detection")
    uploaded_file = st.file_uploader("Upload an image for detection", type=["jpg", "jpeg", "png"])
    confidence_threshold = st.slider("Confidence Threshold:", 0.0, 1.0, 0.25)
    
    if uploaded_file is not None:
        image = uploaded_file.read()
        results = detect_ppe(image, confidence_threshold)
        st.image(results['image'], caption='Uploaded Image with Annotations', use_column_width=True)
        st.write("Detection Results:", results['detections'])

elif options == "Dashboard":
    st.header("Dashboard & Analytics")
    # Placeholder for future dashboard implementation
    st.write("Real-time compliance statistics will be displayed here.")