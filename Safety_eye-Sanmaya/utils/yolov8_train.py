from ultralytics import YOLO

def train_model(epochs, batch):
    model = YOLO("yolov8n.pt")
    model.train(data="configs/dataset.yaml", epochs=epochs, imgsz=640, batch=batch)
