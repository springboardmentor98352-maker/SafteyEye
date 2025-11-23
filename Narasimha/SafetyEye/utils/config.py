# Configuration constants and settings for the SafetyEye application

# Model configuration
MODEL_NAME = "YOLOv8"
MODEL_PATH = "models/safety_detector/best.pt"

# Training parameters
EPOCHS = 100
BATCH_SIZE = 16
IMAGE_SIZE = 640
LEARNING_RATE = 0.001

# Data paths
RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"

# Confidence threshold for detection
CONFIDENCE_THRESHOLD = 0.25

# Logging settings
LOGGING_ENABLED = True
LOGGING_LEVEL = "INFO"

# Dashboard settings
DASHBOARD_PORT = 5000

# Safety classes
SAFETY_CLASSES = {
    "compliant": ["Hardhat", "Safety Vest", "Mask"],
    "violations": ["NO-Hardhat", "NO-Safety Vest", "NO-Mask"],
    "other": ["Person", "Safety Cone", "Machinery", "Vehicle"]
}