import cv2
import numpy as np
import torch

class SafetyDetector:
    def __init__(self, model_path, device='cpu'):
        self.device = device
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        model.eval()
        return model

    def detect(self, image):
        results = self.model(image)
        return results

    def process_results(self, results, confidence_threshold=0.25):
        detections = []
        for *box, conf, cls in results.xyxy[0]:
            if conf >= confidence_threshold:
                detections.append({
                    'box': box.tolist(),
                    'confidence': conf.item(),
                    'class': int(cls.item())
                })
        return detections

    def annotate_image(self, image, detections):
        for detection in detections:
            x1, y1, x2, y2 = map(int, detection['box'])
            label = f'Class: {detection["class"]}, Conf: {detection["confidence"]:.2f}'
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        return image

    def detect_and_annotate(self, image, confidence_threshold=0.25):
        results = self.detect(image)
        detections = self.process_results(results, confidence_threshold)
        annotated_image = self.annotate_image(image, detections)
        return annotated_image, detections