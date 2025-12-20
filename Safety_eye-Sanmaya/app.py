import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
import tempfile
from PIL import Image

# ---------------------------
# Load Model
# ---------------------------
MODEL_PATH = "runs/detect/construction_ppe_model/weights/best.pt"
model = YOLO(MODEL_PATH)

# Class names (from your data.yaml)
CLASS_NAMES = [
    "Hardhat", "Mask", "NO-Hardhat", "NO-Mask", "NO-Safety Vest",
    "Person", "Safety Cone", "Safety Vest", "machinery", "vehicle"
]

VIOLATION_CLASSES = {
    2: "NO-Hardhat",
    3: "NO-Mask",
    4: "NO-Safety Vest"
}

# ---------------------------
# Streamlit UI Setup
# ---------------------------
st.set_page_config(page_title="SafetyEye PPE Detection", layout="wide")

st.title("🦺 SafetyEye – PPE Detection System")
st.write("Upload an image/video or use webcam to detect PPE compliance.")

option = st.sidebar.selectbox(
    "Select Mode",
    ("Image Detection", "Video Detection", "Webcam (Live Detection)")
)

conf_threshold = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.35)

# ---------------------------
# Helper: Draw Boxes + Violations
# ---------------------------
def annotate_image(result):
    img = result.plot()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def check_violations(result):
    violations = []
    if result.boxes:
        classes = result.boxes.cls.cpu().numpy().astype(int)
        for cls in classes:
            if cls in VIOLATION_CLASSES:
                violations.append(VIOLATION_CLASSES[cls])
    return violations

# ---------------------------
# IMAGE MODE
# ---------------------------
if option == "Image Detection":
    st.header("📷 Image PPE Detection")

    uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded is not None:
        img = Image.open(uploaded)
        st.image(img, caption="Uploaded Image", width=500)

        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        results = model.predict(img_cv, conf=conf_threshold)
        annotated = annotate_image(results[0])
        violations = check_violations(results[0])

        st.subheader("🔍 Detection Result")
        st.image(annotated, use_column_width=True)

        if len(violations) > 0:
            st.error("⚠️ Violations Detected:")
            for v in violations:
                st.write("- " + v)
        else:
            st.success("✅ No PPE Violations Detected!")

# ---------------------------
# VIDEO MODE
# ---------------------------
elif option == "Video Detection":
    st.header("🎞 Video PPE Detection")

    uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

    if uploaded_video is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())

        st.info("Processing video... please wait ⏳")

        cap = cv2.VideoCapture(tfile.name)
        output_frames = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model.predict(frame, conf=conf_threshold, verbose=False)
            annotated = results[0].plot()
            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            output_frames.append(annotated_rgb)

        cap.release()

        st.success("Video Processed 🎉")
        st.write("Showing first frame below:")
        st.image(output_frames[0], use_column_width=True)

        st.warning("⚠️ Full video rendering can be added if you want.")

# ---------------------------
# WEBCAM MODE
# ---------------------------
elif option == "Webcam (Live Detection)":
    st.header("🎥 Webcam Live PPE Detection")

    st.warning("Webcam may not work inside some Jupyter environments. Better run using command line.")

    run_webcam = st.button("Start Webcam")

    if run_webcam:
        st.info("Opening webcam... press Q in the window to quit")

        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model.predict(frame, conf=conf_threshold, verbose=False)
            annotated = results[0].plot()

            cv2.imshow("SafetyEye Live", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
