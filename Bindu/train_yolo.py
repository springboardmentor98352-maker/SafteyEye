from ultralytics import YOLO

# Load model (YOLOv8n recommended)
model = YOLO("yolov8n.pt")

# Train
model.train(
    data="ppe_data.yaml",
    epochs=50,
    imgsz=640,
    batch=8
)
