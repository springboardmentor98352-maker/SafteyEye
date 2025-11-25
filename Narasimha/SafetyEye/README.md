# SafetyEye - AI-Powered Workplace Occupancy & Safety Monitor

An AI-based system that uses computer vision and YOLOv8 to monitor workplace occupancy levels and detect safety compliance violations in real-time.

## Project Overview

SafetyEye helps office and industrial space managers improve space utilization and ensure employees follow safety protocols such as wearing helmets, vests, and masks.

## Features

### 1. Data Preparation Module
- Download Construction Site Safety dataset from Kaggle
- Process YOLO-formatted images and labels
- View dataset statistics (train/validation/test splits)
- Support for 10 safety classes

### 2. Model Training Module
- Train custom YOLOv8 models (nano, small, medium)
- Configurable training parameters (epochs, batch size, image size)
- Real-time training progress monitoring
- Automatic model saving and versioning

### 3. Live Detection Module
- Upload images for real-time PPE detection
- Adjustable confidence threshold
- Visual annotations with bounding boxes
- Detailed violation reporting

### 4. Dashboard & Analytics
- Real-time compliance statistics
- Violation type distribution charts
- Compliance trend analysis
- Detection count by safety class

## Safety Classes

### Compliant Classes
- ✅ Hardhat
- ✅ Safety Vest
- ✅ Mask

### Violation Classes
- ❌ NO-Hardhat
- ❌ NO-Safety Vest
- ❌ NO-Mask

### Other Classes
- 👤 Person
- 🚧 Safety Cone
- 🏗️ Machinery
- 🚗 Vehicle

## Dataset

**Source:** [Construction Site Safety Image Dataset](https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow)
- **Provider:** Roboflow Universe Projects
- **Format:** YOLO (images + .txt labels)
- **Classes:** 10
- **Images:** 5000+ annotated images
- **License:** CC BY 4.0
- **Splits:** Training, Validation, Test

## Technology Stack

- **Frontend:** Streamlit
- **AI Model:** YOLOv8 (Ultralytics)
- **Computer Vision:** OpenCV
- **Deep Learning:** PyTorch
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly, Matplotlib
- **Data Source:** Kaggle API

## Installation

### Prerequisites
- Python 3.11+
- Kaggle account and API credentials

### Dependencies
```bash
pip install streamlit ultralytics opencv-python-headless torch torchvision kaggle pillow plotly pandas numpy matplotlib pyyaml
```

## Setup Instructions

### 1. Kaggle API Configuration

To download the dataset, you need Kaggle API credentials:

1. Go to https://www.kaggle.com/
2. Click on your profile picture → Account
3. Scroll to 'API' section
4. Click 'Create New API Token'
5. Download `kaggle.json` file
6. Place it in `~/.kaggle/kaggle.json` or upload via the app interface

### 2. Run the Application

```bash
streamlit run app.py --server.port 5000
```

### 3. Use the Application

1. **Data Preparation:** Download and verify the dataset
2. **Model Training:** Train YOLOv8 on safety classes
3. **Live Detection:** Upload images to detect violations
4. **Dashboard:** View analytics and compliance metrics

## Project Structure

```
SafetyEye/
├── app.py                      # Main Streamlit application
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
├── configs/
│   └── yolov8.yaml            # YOLOv8 configuration settings
├── utils/
│   ├── config.py              # Configuration and constants
│   ├── data_loader.py         # Dataset download and management
│   ├── detector.py            # Safety detection engine
│   └── trainer.py             # Model training utilities
├── models/
│   └── safety_detector/
│       └── README.md          # Trained model weights documentation
├── data/
│   ├── raw/                   # Raw dataset from Kaggle
│   └── processed/             # Processed data
├── notebooks/
│   └── exploratory.ipynb      # Exploratory data analysis notebook
├── tests/
│   ├── test_detector.py       # Unit tests for detection engine
│   └── test_data_loader.py    # Unit tests for data loading utilities
└── docs/
    └── architecture.md         # Application architecture documentation
```

## Usage Guide

### Data Preparation
1. Navigate to "Data Preparation" page
2. Upload `kaggle.json` or configure API credentials
3. Click "Download Dataset" button
4. Wait for download and extraction to complete
5. Verify dataset statistics

### Model Training
1. Navigate to "Model Training" page
2. Select model size (nano for speed, medium for accuracy)
3. Configure training parameters:
   - Epochs: 50-100 (higher = better accuracy, longer training)
   - Image Size: 640 (standard for YOLO)
   - Batch Size: 16 (adjust based on GPU memory)
4. Click "Start Training"
5. Monitor training progress
6. Wait for completion (may take 30+ minutes)

### Live Detection
1. Navigate to "Live Detection" page
2. Upload a construction site or workplace image
3. Adjust confidence threshold (0.25 default)
4. View detection results with annotations
5. Review safety violations and compliance rate

### Dashboard
1. Navigate to "Dashboard & Analytics" page
2. View overall compliance statistics
3. Analyze violation type distribution
4. Track compliance trends over time

## Model Training Notes

- **Quick Testing:** Use 10-20 epochs with yolov8n (nano)
- **Production Use:** Use 50-100+ epochs with yolov8s or yolov8m
- **GPU Recommended:** Training is much faster with GPU support
- **Memory:** Reduce batch size if you encounter out-of-memory errors

## Safety Violation Detection

The system identifies three main violation types:
1. **NO-Hardhat:** Workers without hard hats in construction zones
2. **NO-Safety Vest:** Workers without high-visibility vests
3. **NO-Mask:** Workers without protective masks (when required)

## Outcomes

- ✅ Identify safety compliance violations (missing helmets, vests, masks)
- ✅ Generate visualizations and alerts to improve safety
- ✅ Present results via real-time dashboard for administrators
- ✅ Track compliance trends and patterns
- ✅ Provide evidence with annotated images

## Future Enhancements

- Live video feed processing from surveillance cameras
- Automated email/SMS notification system
- Historical analytics with heatmaps
- Multi-camera support for large facilities
- PDF report generation
- Zone-based monitoring
- Real-time streaming dashboard

## License

This project uses the Construction Site Safety dataset under CC BY 4.0 license.

## Citation

```
@misc{ construction-site-safety_dataset,
    title = { Construction Site Safety Dataset },
    type = { Open Source Dataset },
    author = { Roboflow Universe Projects },
    howpublished = { \url{ https://universe.roboflow.com/roboflow-universe-projects/construction-site-safety } },
    url = { https://universe.roboflow.com/roboflow-universe-projects/construction-site-safety },
    journal = { Roboflow Universe },
    publisher = { Roboflow },
    year = { 2023 },
    month = { feb },
    note = { visited on 2023-02-23 },
}
```

## Support

For issues or questions:
- Check dataset documentation on Kaggle
- Review YOLOv8 documentation at Ultralytics
- Verify Kaggle API credentials are correctly configured