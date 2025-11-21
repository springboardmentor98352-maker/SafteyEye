import streamlit as st
from pathlib import Path

def app():
    st.header('⚙️ Settings')
    st.write('Configure cameras, model confidence, and notification channels.')

    st.subheader('Camera Feeds')
    cam_file = Path('camera_feeds.yaml')
    st.text_area('camera_feeds.yaml', value=cam_file.read_text() if cam_file.exists() else '# camera1: rtsp://...', height=120)

    st.subheader('Model settings')
    st.slider('Confidence threshold', 0.0, 1.0, 0.35)

    st.subheader('Notifications')
    st.checkbox('Enable email alerts', value=False)
