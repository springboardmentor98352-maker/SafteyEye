# SafetyEye 
### AI-Powered Workplace Safety & Occupancy Monitoring System

SafetyEye is an AI-based real-time workplace monitoring system that uses computer vision to detect PPE (Personal Protective Equipment) violations and track occupancy from video surveillance feeds. The system is designed to help industrial and construction site managers improve safety compliance and monitor space utilization.

---

##  Key Features
- Real-time PPE violation detection (Helmet, Mask, Safety Vest)
- Person detection and occupancy counting
- Temporal logic to reduce false alerts
- Live dashboard with alerts and compliance statistics
- Multi-camera support
- Risk-based alert classification

---

##  Technologies Used
- **Deep Learning:** YOLOv8 (Ultralytics)
- **Backend:** Python, Flask, Socket.IO
- **Frontend:** React.js
- **Computer Vision:** OpenCV
- **Dataset:** Construction Site Safety Image Dataset (Roboflow / Kaggle)

---

##  Dataset
- Dataset: Construction Site Safety Image Dataset  
- Source: https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow
- Classes: Helmet, Mask, Safety Vest, NO-Helmet, NO-Mask, NO-Safety Vest, Person, Machinery, Vehicle

---

##  System Architecture
1. Video feed input (CCTV / recorded video)
2. YOLOv8 model performs object detection
3. Violation logic checks for missing PPE
4. Backend processes alerts and metrics
5. Frontend displays live feed, alerts, and analytics

---

##  Model Performance
- Precision: ~90.5%
- Recall: ~77.4%
- mAP@50: ~84.9%
- Inference Speed: ~5 ms per frame

---

##  How to Run the Project

### Backend
pip install -r requirements.txt
python app.py

### Frontend
npm install
npm start
