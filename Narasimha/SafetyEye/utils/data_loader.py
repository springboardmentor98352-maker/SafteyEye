import os
import zipfile
import requests
import pandas as pd
from pathlib import Path

class DataLoader:
    def __init__(self, dataset_url, raw_data_dir, processed_data_dir):
        self.dataset_url = dataset_url
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_data_dir = Path(processed_data_dir)
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)

    def download_dataset(self):
        response = requests.get(self.dataset_url)
        zip_file_path = self.raw_data_dir / 'dataset.zip'
        
        with open(zip_file_path, 'wb') as f:
            f.write(response.content)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(self.raw_data_dir)

        os.remove(zip_file_path)

    def load_yolo_data(self):
        images = []
        labels = []
        
        for label_file in self.raw_data_dir.glob('*.txt'):
            with open(label_file, 'r') as f:
                label_data = f.readlines()
                labels.append(label_data)

            image_file = label_file.with_suffix('.jpg')
            if image_file.exists():
                images.append(image_file)

        return images, labels

    def preprocess_data(self):
        images, labels = self.load_yolo_data()
        # Add preprocessing steps here (e.g., resizing, normalization)
        # For now, just return the loaded data
        return images, labels

    def get_dataset_statistics(self):
        images, labels = self.load_yolo_data()
        return {
            'num_images': len(images),
            'num_labels': len(labels),
        }