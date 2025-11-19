from ultralytics import YOLO
import shutil

print("⬇️ Downloading YOLOv8n pretrained model...")
model = YOLO("yolov8n.pt")
print("✅ Model downloaded successfully!")

# Rename it as best.pt for your app
shutil.copy("yolov8n.pt", "best.pt")
print("✅ Model saved locally as 'best.pt'")
