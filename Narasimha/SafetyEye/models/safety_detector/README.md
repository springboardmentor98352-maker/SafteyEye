# Safety Detector Model Documentation

## Overview

The Safety Detector model is a custom YOLOv8 implementation designed to identify safety compliance violations in workplace environments, particularly in construction sites. This model is trained to detect personal protective equipment (PPE) such as hard hats, safety vests, and masks, as well as violations when these items are not worn.

## Model Details

- **Model Architecture:** YOLOv8
- **Classes Detected:**
  - Compliant:
    - Hardhat
    - Safety Vest
    - Mask
  - Violations:
    - NO-Hardhat
    - NO-Safety Vest
    - NO-Mask
  - Other Classes:
    - Person
    - Safety Cone
    - Machinery
    - Vehicle

## Usage Instructions

1. **Loading the Model:**
   To use the trained model for detection, load the model weights from the `models/safety_detector` directory.

2. **Performing Detection:**
   Utilize the detection functions provided in the `utils/detector.py` file. Pass the input image to the detection function, and it will return the detected objects along with their bounding boxes and confidence scores.

3. **Visualizing Results:**
   The model provides visual annotations on the detected objects. You can use OpenCV or Matplotlib to display the results.

## Training Information

- **Training Dataset:** The model is trained on the Construction Site Safety dataset, which includes over 5000 annotated images.
- **Training Parameters:**
  - Epochs: Configurable (recommended: 50-100 for production)
  - Batch Size: Configurable (adjust based on GPU memory)
  - Image Size: Standard size of 640 for YOLO

## Future Improvements

- Enhance model accuracy with additional training data.
- Implement real-time video feed processing.
- Expand detection capabilities to include more safety classes.

## License

This model is trained using the Construction Site Safety dataset under the CC BY 4.0 license. Please refer to the dataset documentation for more details.