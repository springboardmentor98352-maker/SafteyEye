import os
import yaml
import streamlit as st
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ultralytics import YOLO

def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Return default config if file doesn't exist
        return {
            'app': {
                'title': 'SafetyEye',
                'version': '1.0.0'
            },
            'model': {
                'default_confidence': 0.5,
                'default_model': 'yolov8s.pt'
            }
        }

def setup_page():
    """Set up the Streamlit page configuration."""
    # Custom CSS for better styling
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        .stMetric {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stAlert {
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

def generate_sample_data(days: int = 7) -> pd.DataFrame:
    """Generate sample violation data for demonstration."""
    np.random.seed(42)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days-1)
    
    date_range = pd.date_range(start_date, end_date, freq='D')
    
    data = {
        'timestamp': [],
        'violation_type': [],
        'confidence': [],
        'location': [],
        'image_path': []
    }
    
    violation_types = ['No Helmet', 'No Vest', 'No Safety Glasses', 'Overcrowding']
    locations = ['Main Entrance', 'Workshop A', 'Workshop B', 'Loading Bay', 'Warehouse']
    
    for date in date_range:
        # Generate between 5-15 violations per day
        num_violations = np.random.randint(5, 16)
        for _ in range(num_violations):
            # Spread timestamps throughout the day
            time_offset = np.random.uniform(0, 1)
            timestamp = date + timedelta(days=time_offset)
            
            data['timestamp'].append(timestamp)
            data['violation_type'].append(np.random.choice(violation_types))
            data['confidence'].append(round(np.random.uniform(0.6, 0.99), 2))
            data['location'].append(np.random.choice(locations))
            data['image_path'].append(f"violation_{int(timestamp.timestamp())}.jpg")
    
    return pd.DataFrame(data).sort_values('timestamp', ascending=False)

def get_violation_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate statistics from violation data."""
    if df.empty:
        return {}
        
    stats = {
        'total_violations': len(df),
        'violations_today': len(df[df['timestamp'].dt.date == datetime.now().date()]),
        'violation_types': df['violation_type'].value_counts().to_dict(),
        'by_location': df['location'].value_counts().to_dict(),
        'by_hour': df['timestamp'].dt.hour.value_counts().sort_index().to_dict(),
        'recent_violations': df.head(10).to_dict('records')
    }
    
    return stats

def load_model(model_path: str):
    """Load YOLO model from the given path."""
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def run_detection(model, frame, confidence_threshold=0.5):
    """Run object detection on a single frame."""
    try:
        # Run YOLO detection
        results = model(frame, conf=confidence_threshold)
        
        # Process results
        detections = []
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()  # x1, y1, x2, y2
            confs = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            
            for box, conf, cls_id in zip(boxes, confs, class_ids):
                x1, y1, x2, y2 = box
                label = model.names[cls_id]  # Get class name
                
                detections.append({
                    'box': (x1, y1, x2, y2),
                    'confidence': float(conf),
                    'class_id': int(cls_id),
                    'label': label
                })
        
        return detections
        
    except Exception as e:
        st.error(f"Error during detection: {str(e)}")
        return []

def get_violation_stats():
    """Get sample violation statistics."""
    df = generate_sample_data()
    return get_violation_stats(df)

def get_logs(limit: int = 100) -> pd.DataFrame:
    """Get sample violation logs."""
    return generate_sample_data(30).head(limit)  # Last 30 days, limited by 'limit'
