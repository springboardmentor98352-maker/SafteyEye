# In pages/3_📋_violation_logs.py
import streamlit as st
import pandas as pd
from PIL import Image
import io

st.set_page_config(
    page_title="Violation Logs - SafetyEye",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Violation Logs")

# Show message if no violations
if 'violations' not in st.session_state or not st.session_state.violations:
    st.info("No violations logged yet. Please run detections in the Live Monitoring or Image Detection page.")
    st.stop()

# Convert to DataFrame for display
df = pd.DataFrame(st.session_state.violations)

# Convert timestamp to string for display
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')

# Show data table
st.subheader("All Detected Violations")
st.dataframe(
    df[['timestamp', 'type', 'confidence']], 
    use_container_width=True,
    column_config={
        "timestamp": "Timestamp",
        "type": "Violation Type",
        "confidence": "Confidence"
    }
)

# Allow exporting the data
if st.button("Export to CSV"):
    csv = df[['timestamp', 'type', 'confidence']].to_csv(index=False)
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="safetyeye_violations.csv",
        mime="text/csv"
    )