# app/backend/utils.py

import cv2
import numpy as np

def read_image(uploaded_file):
    """Convert Streamlit uploaded file into OpenCV image."""
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return img
