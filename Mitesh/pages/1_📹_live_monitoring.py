# In pages/1_📹_live_monitoring.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils.helpers import load_model, run_detection
from datetime import datetime
import time
import os
import tempfile

# Page configuration
st.set_page_config(
    page_title="Live Monitoring - SafetyEye",
    page_icon="📹",
    layout="wide"
)

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.model_loaded = False
if 'violations' not in st.session_state:
    st.session_state.violations = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'temp_video_path' not in st.session_state:
    st.session_state.temp_video_path = None

# Page title
st.title("📹 Safety Monitoring with YOLO Model")

# Video uploader
video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mpeg4"], help="Upload a video file for safety monitoring analysis")

# Handle video file - save uploaded file to temporary location
video_path = None
if video_file is not None:
    # Clean up old temporary file if exists
    if st.session_state.temp_video_path and os.path.exists(st.session_state.temp_video_path):
        try:
            os.unlink(st.session_state.temp_video_path)
        except:
            pass
    
    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(video_file.name)[1]) as tmp_file:
        tmp_file.write(video_file.getbuffer())
        video_path = tmp_file.name
        st.session_state.temp_video_path = video_path
    st.success(f"Video uploaded: {video_file.name}")
else:
    # Check if we have a previously uploaded video in session state
    if st.session_state.temp_video_path and os.path.exists(st.session_state.temp_video_path):
        video_path = st.session_state.temp_video_path
    else:
        # Use sample video if no file uploaded
        sample_path = "sample_safety.mp4"
        if os.path.exists(sample_path):
            video_path = sample_path
        else:
            st.info("Please upload a video file to start processing.")
            video_path = None

# Sidebar controls
st.sidebar.header("Detection Controls")

# Model path
model_path = "models/best (8).pt"

# Confidence threshold
confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.1,
    max_value=0.99,
    value=0.5,
    step=0.05
)

# Start/Stop button
stop_processing = st.sidebar.checkbox("Stop Processing", value=False)
if stop_processing:
    st.session_state.processing = False
else:
    if st.sidebar.button("▶️ Start Processing" if not st.session_state.processing else "⏹️ Stop Processing"):
        st.session_state.processing = not st.session_state.processing
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🚨 Detected Violations")
violation_placeholder = st.sidebar.empty()

# Function to process a single frame
def process_frame(frame, model, confidence_threshold=0.5):
    if model is not None and frame is not None:
        # Convert frame to RGB (YOLO expects RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Run detection
        detections = run_detection(model, frame_rgb, confidence_threshold)
        
        # Process detections
        for det in detections:
            x1, y1, x2, y2 = map(int, det['box'])
            label = det['label']
            conf = det['confidence']
            
            # Draw rectangle (red for violations, green for compliance)
            color = (0, 0, 255) if "No " in label else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Add label
            label_text = f"{label} {conf:.2f}"
            cv2.putText(
                frame, 
                label_text, 
                (x1, y1 - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                color, 
                2
            )
            
            # Log violation if it's a safety violation
            if "No " in label:
                violation = {
                    'timestamp': datetime.now(),
                    'type': label,
                    'confidence': conf,
                    'frame': frame.copy()
                }
                if 'violations' not in st.session_state:
                    st.session_state.violations = []
                st.session_state.violations.append(violation)
                violation_placeholder.warning(
                    f"**{label}** detected!\n"
                    f"Confidence: {conf:.2f}\n"
                    f"Time: {violation['timestamp'].strftime('%H:%M:%S')}"
                )
    
    return frame

# Main processing function
def process_video(video_path_arg, confidence_threshold):
    # Validate video path
    if video_path_arg is None or not os.path.exists(video_path_arg):
        st.error("No valid video file selected. Please upload a video file.")
        st.session_state.processing = False
        st.rerun()
        return
    
    # Load model if not already loaded
    model_path = "models/best (8).pt"
    if not st.session_state.model_loaded:
        with st.spinner("Loading YOLO model..."):
            st.session_state.model = load_model(model_path)
            st.session_state.model_loaded = True
            if not st.session_state.model:
                st.sidebar.error("Failed to load model!")
                st.session_state.processing = False
                st.rerun()
                return
    
    # Open video file
    try:
        # Ensure we have a string path (not None or other type)
        if not isinstance(video_path_arg, str):
            st.error("Invalid video path type. Please upload a valid video file.")
            st.session_state.processing = False
            st.rerun()
            return
            
        cap = cv2.VideoCapture(video_path_arg)
        if not cap.isOpened():
            st.error(f"Error: Could not open video file. Please ensure the file is a valid video format.")
            st.session_state.processing = False
            st.rerun()
            return
    except Exception as e:
        st.error(f"Error opening video: {str(e)}")
        st.session_state.processing = False
        st.rerun()
        return
    
    frame_placeholder = st.empty()
    frame_count = 0
    
    try:
        while st.session_state.processing and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.info("End of video reached.")
                break
                
            frame_count += 1
            
            # Process frame
            processed_frame = process_frame(frame, st.session_state.model, confidence_threshold)
            
            # Display the processed frame
            frame_placeholder.image(processed_frame, channels="BGR", use_container_width=True)
            
            # Small delay to control playback speed
            time.sleep(0.03)  # ~30 FPS
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")
        st.session_state.processing = False
    finally:
        cap.release()
    
    if not st.session_state.processing:
        st.rerun()

# Start processing if button is pressed
if st.session_state.processing and video_path:
    process_video(video_path, confidence)
elif st.session_state.processing and not video_path:
    st.warning("Please upload a video file first.")
    st.session_state.processing = False
    st.rerun()

# Display recent violations
st.markdown("---")
st.subheader("Recent Violations")

if 'violations' in st.session_state and st.session_state.violations:
    cols = st.columns(3)
    for i, violation in enumerate(reversed(st.session_state.violations[-6:])):
        with cols[i % 3]:
            # Convert the frame to RGB if it's not already
            if isinstance(violation['frame'], np.ndarray):
                if len(violation['frame'].shape) == 3:  # If it's a color image
                    if violation['frame'].shape[2] == 4:  # If RGBA
                        img_rgb = cv2.cvtColor(violation['frame'], cv2.COLOR_RGBA2RGB)
                    else:  # If BGR
                        img_rgb = cv2.cvtColor(violation['frame'], cv2.COLOR_BGR2RGB)
                else:  # If grayscale
                    img_rgb = cv2.cvtColor(violation['frame'], cv2.COLOR_GRAY2RGB)
                
                # Convert to PIL Image
                img = Image.fromarray(img_rgb)
                
                st.image(
                    img, 
                    width=200, 
                    caption=f"{violation['type']} - {violation['confidence']:.2f}\n"
                          f"{violation['timestamp'].strftime('%H:%M:%S')}"
                )
            else:
                st.warning("Invalid frame format in violation record")
else:
    st.info("No violations detected yet. Upload a video and click 'Start Processing'.")

# Add a footer
st.markdown("---")
st.caption("SafetyEye - Real-time Safety Monitoring with YOLO")