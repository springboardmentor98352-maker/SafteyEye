# SafetyEye: AI-Powered PPE Monitoring System 🛡️

![SafetyEye Banner](https://img.shields.io/badge/AI-Powered-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![YOLOv8](https://img.shields.io/badge/YOLOv8-Object_Detection-orange) ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

SafetyEye is an advanced computer vision application designed to enhance workplace safety. It uses state-of-the-art AI (YOLOv8) to monitor Personal Protective Equipment (PPE) compliance in real-time.

## 🚀 Key Features

*   **⚡ Real-Time Detection:** Instantly identifies people and PPE (Hardhats, Masks, Safety Vests).
*   **🎥 Live Video Analysis:** Connects to standard webcams for continuous monitoring.
*   **📊 Dynamic Reporting:** Generates real-time analytics, compliance rates, and violation trends.
*   **💾 Video Processing:** Upload and analyze pre-recorded footage with "Ultra-Fast" processing logic.
*   **📉 Historical Data:** Automatically saves and organizes detection sessions for review.
*   **📱 Responsive Dashboard:** A modern, user-friendly interface powered by Streamlit.

## 🛠️ Technology Stack

*   **Core Engine:** Python 3.8+
*   **AI Model:** YOLOv8 (Ultralytics)
*   **Interface:** Streamlit
*   **Computer Vision:** OpenCV (cv2)
*   **Visualization:** Plotly, PIL

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/safetyeye-ppe-monitor.git
    cd safetyeye-ppe-monitor
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download the Model:**
    Ensure you have the `best.pt` model file in the `models/` directory.

## 🚦 Usage

Run the application with a single command:

```bash
streamlit run app_ultra_fast.py
```

Navigate to `http://localhost:8501` in your browser.

## 📋 Features in Detail

### 1. Live Detection
Connect your webcam to start monitoring. The system draws bounding boxes:
*   🟢 **Green:** Compliant (PPE Detected)
*   🔴 **Red:** Violation (Missing PPE)

### 2. Video Analysis
Upload MP4 or AVI files. The system processes them at accelerated speeds, providing a downloadable analysis report upon completion.

### 3. Results History
View past sessions, compare compliance rates, and download detailed JSON logs of every detection event.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
