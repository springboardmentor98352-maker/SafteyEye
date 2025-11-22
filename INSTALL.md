# SafetyEye Installation Guide

## Quick Start

The SafetyEye application is ready to use! Follow these steps:

### 1. Configure Kaggle API

To download the dataset, you need Kaggle API credentials:

1. Go to https://www.kaggle.com/
2. Sign in and go to Account Settings
3. Scroll to "API" section
4. Click "Create New API Token"
5. Download `kaggle.json` file
6. Upload it via the app interface or set as environment variables

### 2. Run the Application

The application is already running on port 5000. Navigate through the pages:

1. **Home** - Overview of the project
2. **Data Preparation** - Download and verify the dataset
3. **Model Training** - Train YOLOv8 model (requires ultralytics)
4. **Live Detection** - Detect safety violations in images
5. **Dashboard** - View analytics and statistics

## Important Notes About Dependencies

### YOLOv8 / Ultralytics Installation

The Ultralytics library (YOLOv8) could not be automatically installed due to dependency conflicts in the current environment. There are two options:

#### Option 1: Manual Installation (Advanced)
If you need full model training capabilities, you can try:
```bash
pip install --no-deps ultralytics torch torchvision
```

However, this may require additional system dependencies and GPU support.

#### Option 2: Use the Application Without Training
You can still use SafetyEye for:
- Data preparation and exploration
- Dataset statistics and visualization
- Dashboard analytics
- Understanding the workflow

The model training and detection features will show helpful error messages guiding you through the requirements.

### Pre-trained Models

If you have a pre-trained YOLOv8 model (`.pt` file), you can:
1. Upload it to the `models/safety_detector/weights/` directory
2. Name it `best.pt`
3. Use it directly for detection

## Dataset Information

- **Name:** Construction Site Safety Image Dataset
- **Source:** Kaggle (Roboflow)
- **Size:** ~228 MB
- **Images:** 2,801 total (2,605 train, 114 validation, 82 test)
- **Format:** YOLO (.txt labels)
- **Classes:** 10 (Hardhat, Mask, NO-Hardhat, NO-Mask, NO-Safety Vest, Person, Safety Cone, Safety Vest, machinery, vehicle)

## System Requirements

- **Python:** 3.11+
- **RAM:** 4GB minimum (8GB+ recommended for training)
- **Storage:** 1GB minimum for dataset
- **GPU:** Recommended for model training (optional for inference)

## Troubleshooting

### Kaggle API Errors
- Ensure `kaggle.json` has correct permissions (600)
- Verify your Kaggle account is active
- Check that you've accepted the dataset's terms on Kaggle

### Dataset Not Found
- The app automatically searches for the dataset in multiple possible locations
- After download, the dataset structure is: `css-data/train`, `css-data/valid`, `css-data/test`

### Model Training Errors
- Ensure Ultralytics is installed
- Check that the dataset is downloaded and verified
- Reduce batch size if you encounter memory errors

## Next Steps

1. Start with **Data Preparation** to download the dataset
2. Explore **Dashboard** to understand the analytics
3. If you need training, set up Ultralytics library
4. Use **Live Detection** with a pre-trained model or train your own

## Support

For detailed information about the project, see the main README.md file.
