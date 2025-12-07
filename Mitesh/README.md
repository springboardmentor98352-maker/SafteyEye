# SafetyEye - AI Powered Workplace Safety Monitor

A real-time workplace safety monitoring system that uses computer vision to detect safety violations such as missing PPE (Personal Protective Equipment) and monitor occupancy levels.

## 🚀 Features

- **Real-time Monitoring**: Live video feed with object detection
- **Safety Violation Detection**: Identify missing PPE (helmets, vests, etc.)
- **Analytics Dashboard**: Visualize safety metrics and trends
- **Violation Logs**: Track and manage safety incidents
- **Exportable Reports**: Generate reports in CSV or Excel format

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/safetyeye.git
   cd safetyeye
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download YOLO model** (or use your own)
   ```bash
   wget https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8s.pt -O models/yolov8s.pt
   ```

## 🚦 Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Access the dashboard**
   Open your web browser and navigate to:
   ```
   http://localhost:8501
   ```

## 📂 Project Structure

```
safetyeye/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── utils/
│   └── helpers.py         # Helper functions and utilities
├── pages/
│   ├── 1_📹_live_monitoring.py  # Live monitoring page
│   ├── 2_📈_analytics.py        # Analytics dashboard
│   └── 3_📋_violation_logs.py   # Violation logs
└── models/                # YOLO model files
```

## 🔌 Integration with YOLO Model

The application is designed to work with YOLOv8 models. To integrate your own model:

1. Place your `.pt` model file in the `models/` directory
2. Update the model path in the Live Monitoring page
3. Implement the detection logic in `utils/helpers.py`

## 📊 Sample Data

The application includes sample data generation for demonstration purposes. In a production environment, you would connect to your actual data source.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For any questions or feedback, please contact [your-email@example.com](mailto:your-email@example.com)
