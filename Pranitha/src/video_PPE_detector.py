from ultralytics import YOLO
import cv2
import os

model = YOLO("models/best.pt")

# Violation rule logic
def check_violations(result):
    names = result.names
    classes = result.boxes.cls.tolist()

    violations = []
    detected = [names[int(c)] for c in classes]

    if "Person" in detected:
        if "No_Hardhat" in detected:
            violations.append("Worker without Helmet")
        if "No_Vest" in detected:
            violations.append("Worker without Safety Vest")
        if "No_Gloves" in detected:
            violations.append("Worker without Gloves")

    return violations


video_path = "data/raw/source_files/source_files/indianworkers.mp4"


if not os.path.exists(video_path):
    print("Video not found:", video_path)
    exit()

# Load video
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Unable to open video")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO prediction on the frame
    results = model.predict(frame, conf=0.5)

    # Draw bounding boxes on frame
    annotated_frame = results[0].plot()

    # Check violations
    violations = check_violations(results[0])

    # Print violations in terminal
    if violations:
        print("Violations:", violations)

    # Show video frame
    cv2.imshow("SafetyEye - Video PPE Analyzer", annotated_frame)

    # Press 'q' to exit early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
