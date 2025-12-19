"""
SafetyEye Detection Engine
Simplified PPE detection engine focused solely on safety monitoring
"""

import cv2
import numpy as np
from ultralytics import YOLO
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SafetyEyeEngine:
    """Simplified PPE detection engine for safety monitoring"""
    
    def __init__(self, model_path: str = "models/best.pt"):
        """Initialize the SafetyEye detection engine
        
        Args:
            model_path: Path to the YOLOv8 model file
        """
        self.model_path = model_path
        self.model = None
        self.class_names = {
            0: 'Hardhat',
            1: 'Mask',
            2: 'NO-Hardhat',
            3: 'NO-Mask',
            4: 'NO-Safety Vest',
            5: 'Person',
            6: 'Safety Cone',
            7: 'Safety Vest',
            8: 'machinery',
            9: 'vehicle'
        }
        
        # Compliance classes - True for required PPE, False for violations
        # This will be updated based on the loaded model
        self.compliance_classes = {
            'Hardhat': True,
            'Mask': True,
            'Safety Vest': True,
            'NO-Hardhat': False,
            'NO-Mask': False,
            'NO-Safety Vest': False
        }
        
        self.load_model()
    
    def _load_fallback_model(self) -> bool:
        """Load a fallback YOLO model for demonstration purposes
        
        Returns:
            bool: True if fallback model loaded successfully, False otherwise
        """
        try:
            logger.info("Loading fallback YOLO model (yolov8n.pt) for demonstration...")
            # Using a small pre-trained model for demonstration
            self.model = YOLO('yolov8n.pt')
            logger.info("Fallback model loaded successfully")
            # Update class names to match COCO dataset
            self.class_names = {
                i: name for i, name in enumerate(self.model.names.values())
            }
            # Update compliance classes for COCO dataset
            # Map COCO classes to our PPE classes where possible
            self.compliance_classes = {
                'person': True,  # We'll treat all persons as compliant for demo
                'hat': False,    # Not wearing hat would be a violation if detected as person
            }
            logger.info("Fallback model configured for demonstration")
            return True
        except Exception as e:
            logger.error(f"Error loading fallback model: {e}")
            logger.error("Please ensure you have internet connectivity to download the fallback model")
            return False
    
    def load_model(self) -> bool:
        """Load the YOLOv8 model
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            # Debug information
            logger.info(f"Current working directory: {os.getcwd()}")
            logger.info(f"Model path specified: {self.model_path}")
            logger.info(f"Absolute model path: {os.path.abspath(self.model_path)}")
            
            if os.path.exists(self.model_path):
                logger.info(f"Model file found at: {self.model_path}")
                try:
                    self.model = YOLO(self.model_path)
                    logger.info("Model loaded successfully")
                    return True
                except Exception as model_error:
                    logger.error(f"Error loading custom YOLO model: {model_error}")
                    logger.error("Attempting to load fallback model...")
                    return self._load_fallback_model()
            else:
                # Check if file exists with absolute path
                abs_path = os.path.abspath(self.model_path)
                if os.path.exists(abs_path):
                    logger.info(f"Model file found at absolute path: {abs_path}")
                    try:
                        self.model = YOLO(abs_path)
                        logger.info("Model loaded successfully")
                        return True
                    except Exception as model_error:
                        logger.error(f"Error loading custom YOLO model: {model_error}")
                        logger.error("Attempting to load fallback model...")
                        return self._load_fallback_model()
                else:
                    logger.warning(f"Custom model file not found at: {self.model_path} or {abs_path}")
                    logger.info("Attempting to load fallback model...")
                    return self._load_fallback_model()
        except Exception as e:
            logger.error(f"Unexpected error loading model: {e}")
            logger.info("Attempting to load fallback model...")
            return self._load_fallback_model()
    
    def detect_objects(self, image: np.ndarray, conf_threshold: float = 0.5,
                      iou_threshold: float = 0.45) -> dict:
        """Detect objects in an image
        
        Args:
            image: Input image as numpy array
            conf_threshold: Confidence threshold for detection
            iou_threshold: IoU threshold for NMS
            
        Returns:
            Dict containing detection results and compliance info
        """
        if self.model is None:
            return {"error": "Model not loaded"}
        
        try:
            # Ensure image has correct number of channels
            if len(image.shape) == 3 and image.shape[2] == 4:
                # Convert RGBA to RGB
                image = image[:, :, :3]
            elif len(image.shape) == 2:
                # Convert grayscale to RGB
                image = np.stack([image] * 3, axis=-1)
            elif len(image.shape) == 3 and image.shape[2] == 1:
                # Convert single channel to RGB
                image = np.repeat(image, 3, axis=2)
            
            # Run inference
            results = self.model(image, conf=conf_threshold, iou=iou_threshold)
            
            # Process results
            detections = []
            people_detections = []
            violation_detections = []
            
            compliance_stats = {
                'total_people': 0,
                'compliant_people': 0,
                'violations': [],
                'compliance_rate': 100.0,
                'people_with_violations': 0
            }
            
            if results and len(results) > 0:
                result = results[0]
                
                if result.boxes is not None:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    confidences = result.boxes.conf.cpu().numpy()
                    class_ids = result.boxes.cls.cpu().numpy().astype(int)
                    
                    # Collect all detections
                    for i, (box, conf, class_id) in enumerate(zip(boxes, confidences, class_ids)):
                        class_name = self.class_names.get(class_id, f"Class_{class_id}")
                        
                        # Handle different class naming conventions
                        # For fallback model, map COCO classes to our expected names
                        mapped_class_name = class_name
                        if class_name.lower() == 'person':
                            mapped_class_name = 'Person'
                        elif class_name.lower() == 'hat':
                            mapped_class_name = 'NO-Hardhat'  # Treat hat detection as violation for demo
                        
                        detection = {
                            'bbox': box.tolist(),
                            'confidence': float(conf),
                            'class_id': int(class_id),
                            'class_name': class_name,
                            'mapped_class_name': mapped_class_name,
                            'is_compliant': self.compliance_classes.get(mapped_class_name, 
                                          self.compliance_classes.get(class_name, None))
                        }
                        detections.append(detection)
                        
                        # Separate people and violations
                        # Use mapped class name for consistency
                        check_class_name = detection.get('mapped_class_name', class_name)
                        if check_class_name == 'Person':
                            people_detections.append(detection)
                        elif check_class_name in ['NO-Hardhat', 'NO-Mask', 'NO-Safety Vest']:
                            violation_detections.append(detection)
                    
                    # Count total people
                    compliance_stats['total_people'] = len(people_detections)
                    
                    # Associate violations with people
                    people_with_violations = set()
                    
                    for violation in violation_detections:
                        violation_bbox = violation['bbox']
                        violation_center = [
                            (violation_bbox[0] + violation_bbox[2]) / 2,
                            (violation_bbox[1] + violation_bbox[3]) / 2
                        ]
                        
                        # Find closest person to this violation
                        min_distance = float('inf')
                        closest_person_idx = -1
                        
                        for i, person in enumerate(people_detections):
                            person_bbox = person['bbox']
                            person_center = [
                                (person_bbox[0] + person_bbox[2]) / 2,
                                (person_bbox[1] + person_bbox[3]) / 2
                            ]
                            
                            # Calculate distance between centers
                            distance = ((violation_center[0] - person_center[0]) ** 2 +
                                      (violation_center[1] - person_center[1]) ** 2) ** 0.5
                            
                            # Check if violation is within reasonable proximity to person
                            person_width = person_bbox[2] - person_bbox[0]
                            person_height = person_bbox[3] - person_bbox[1]
                            max_distance = max(person_width, person_height) * 1.5
                            
                            if distance < min_distance and distance < max_distance:
                                min_distance = distance
                                closest_person_idx = i
                        
                        # Associate the violation
                        if closest_person_idx >= 0:
                            people_with_violations.add(closest_person_idx)
                            compliance_stats['violations'].append({
                                'type': violation['class_name'],
                                'bbox': violation['bbox'],
                                'confidence': violation['confidence'],
                                'associated_person_idx': closest_person_idx
                            })
                        else:
                            # Violation without associated person
                            compliance_stats['violations'].append({
                                'type': violation['class_name'],
                                'bbox': violation['bbox'],
                                'confidence': violation['confidence'],
                                'associated_person_idx': -1
                            })
                    
                    # Calculate compliance statistics
                    compliance_stats['people_with_violations'] = len(people_with_violations)
                    
                    if compliance_stats['total_people'] > 0:
                        compliance_stats['compliant_people'] = compliance_stats['total_people'] - compliance_stats['people_with_violations']
                        compliance_stats['compliance_rate'] = (compliance_stats['compliant_people'] / compliance_stats['total_people']) * 100
                    else:
                        compliance_stats['compliant_people'] = 0
                        compliance_stats['compliance_rate'] = 100.0
            
            return {
                'detections': detections,
                'compliance_stats': compliance_stats,
                'image_shape': image.shape
            }
            
        except Exception as e:
            error_msg = f"Detection failed: {str(e)}"
            if hasattr(image, 'shape'):
                error_msg += f" (Image shape: {image.shape})"
            logger.error(error_msg)
            return {"error": error_msg}
    
    def draw_detections(self, image: np.ndarray, detections: list,
                       show_confidence: bool = True) -> np.ndarray:
        """Draw detection results on image
        
        Args:
            image: Input image
            detections: List of detection dictionaries
            show_confidence: Whether to show confidence scores
            
        Returns:
            Image with drawn detections
        """
        result_image = image.copy()
        
        # Define colors for different classes
        colors = {
            'Hardhat': (0, 255, 0),      # Green
            'Mask': (0, 255, 0),         # Green
            'Safety Vest': (0, 255, 0),  # Green
            'NO-Hardhat': (0, 0, 255),   # Red
            'NO-Mask': (0, 0, 255),      # Red
            'NO-Safety Vest': (0, 0, 255), # Red
            'Person': (255, 255, 0),     # Yellow
            'Safety Cone': (255, 165, 0), # Orange
            'machinery': (128, 0, 128),   # Purple
            'vehicle': (255, 192, 203)    # Pink
        }
        
        for detection in detections:
            bbox = detection['bbox']
            class_name = detection['class_name']
            confidence = detection['confidence']
            
            # Get color
            color = colors.get(class_name, (128, 128, 128))  # Default gray
            
            # Draw bounding box
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(result_image, (x1, y1), (x2, y2), color, 2)
            
            # Prepare label
            label = class_name
            if show_confidence:
                label += f" {confidence:.2f}"
            
            # Draw label
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            label_x1 = x1
            label_y1 = y1 - label_size[1] - 10
            label_x2 = x1 + label_size[0] + 8
            label_y2 = y1
            
            # Draw label background
            cv2.rectangle(result_image, (label_x1, label_y1), (label_x2, label_y2), color, -1)
            
            # Draw label text
            cv2.putText(result_image, label, (x1 + 4, y1 - 6),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return result_image