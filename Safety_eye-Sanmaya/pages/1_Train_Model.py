import streamlit as st
from utils.yolov8_train import train_model

st.title("Train YOLOv8 Model 🏋️")

epochs = st.slider("Epochs", 10, 200, 50)
batch = st.slider("Batch Size", 4, 32, 8)

if st.button("Start Training 🚀"):
    with st.spinner("Training in progress..."):
        train_model(epochs, batch)
    st.success("Training Completed 🎉")
