# Architecture of SafetyEye

## Overview

SafetyEye is an AI-powered workplace occupancy and safety monitoring system that leverages computer vision and deep learning techniques to ensure compliance with safety protocols in real-time. The architecture is designed to facilitate modularity, scalability, and ease of maintenance.

## Components

### 1. User Interface (UI)
- **Streamlit Application (app.py)**: The main entry point for users to interact with the system. It provides a web-based interface for data preparation, model training, live detection, and analytics.

### 2. Data Management
- **Data Loader (utils/data_loader.py)**: Responsible for downloading and managing the dataset. It handles the preprocessing of YOLO-formatted images and labels, ensuring that the data is ready for training and evaluation.
- **Data Directories**:
  - **raw/**: Contains the original dataset downloaded from Kaggle.
  - **processed/**: Holds the processed data that is ready for model training.

### 3. Model Training
- **Trainer (utils/trainer.py)**: Contains utilities for training the YOLOv8 model. It manages training parameters such as epochs, batch size, and image size, and handles model saving and versioning.

### 4. Detection Engine
- **Detector (utils/detector.py)**: Implements the safety detection engine using the trained YOLOv8 model. It performs real-time detection of personal protective equipment (PPE) and generates visual annotations for compliance violations.

### 5. Configuration
- **Configuration File (configs/yolov8.yaml)**: Contains all the necessary configuration settings for the YOLOv8 model, including parameters for training and detection.

### 6. Analytics and Reporting
- **Dashboard & Analytics**: Provides real-time compliance statistics, violation type distribution, and trend analysis through visualizations. This is integrated into the Streamlit application for user access.

## Data Flow

1. **Data Preparation**: Users initiate the data preparation process through the UI, which triggers the data loader to download and preprocess the dataset.
2. **Model Training**: Once the data is prepared, users can configure training parameters and start training the YOLOv8 model. The trainer manages this process and saves the trained model weights.
3. **Live Detection**: Users can upload images for real-time PPE detection. The detector processes these images and provides visual feedback on compliance.
4. **Analytics**: The dashboard aggregates data from the detection engine and presents it to users, allowing them to monitor compliance trends and generate reports.

## Future Enhancements

- Integration of live video feed processing for continuous monitoring.
- Implementation of automated notification systems for compliance violations.
- Expansion of analytics capabilities with historical data and heatmaps.
- Support for multi-camera setups in larger facilities.

This architecture ensures that SafetyEye remains flexible and can adapt to future requirements while providing a robust solution for workplace safety monitoring.