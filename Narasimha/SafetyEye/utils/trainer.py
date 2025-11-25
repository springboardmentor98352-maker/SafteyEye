import os
import torch
from ultralytics import YOLO

class ModelTrainer:
    def __init__(self, model_size='yolov8n', epochs=50, batch_size=16, image_size=640, save_dir='models/safety_detector'):
        self.model_size = model_size
        self.epochs = epochs
        self.batch_size = batch_size
        self.image_size = image_size
        self.save_dir = save_dir
        self.model = None

    def load_model(self):
        self.model = YOLO(self.model_size)

    def train(self, train_data, val_data):
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() before training.")

        self.model.train(data=train_data, epochs=self.epochs, batch=self.batch_size, imgsz=self.image_size, val=val_data)
        self.save_model()

    def save_model(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self.model.save(os.path.join(self.save_dir, f'{self.model_size}_trained.pt'))

    def load_trained_model(self, model_path):
        if os.path.exists(model_path):
            self.model = YOLO(model_path)
        else:
            raise FileNotFoundError(f"Model file not found: {model_path}")