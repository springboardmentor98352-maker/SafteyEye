import streamlit as st
from PIL import Image
import numpy as np
import time
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="SafetyEye PPE Monitor", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
.metric-card {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}
.warning {
    color: #ff4b4b;
    font-weight: bold;
}
.success {
    color: #00cc00;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🛡️ SafetyEye – AI-Powered Safety Monitor")
st.markdown("---")

# Sidebar menu
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Dashboard", "Real-time Monitoring", "Violation Reports", "Settings"])

# Sample data for demonstration
ppe_classes = ['Helmet', 'Vest', 'Gloves', 'Boots', 'Goggles']
sample_violations = [
    {'time': '10:15 AM', 'location': 'Zone A', 'person_id': 'EMP-012', 'violations': ['No Helmet']},
    {'time': '10:08 AM', 'location': 'Zone B', 'person_id': 'EMP-008', 'violations': ['No Vest']},
    {'time': '09:45 AM', 'location': 'Zone C', 'person_id': 'EMP-021', 'violations': ['No Helmet', 'No Vest']},
    {'time': '09:30 AM', 'location': 'Zone A', 'person_id': 'EMP-017', 'violations': ['No Gloves']},
]

# Dashboard Page
if page == "Dashboard":
    st.header("🏢 Workplace Safety Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Occupancy", "42", "3")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Compliance Rate", "87%", "2%")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Active Alerts", "3", delta="-2", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Today's Violations", "12", delta="-3", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Compliance charts
    st.subheader("📊 Safety Compliance Trends")
    
    # Generate sample compliance data
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    helmet_data = [85, 87, 89, 86, 90, 92, 87]
    vest_data = [80, 82, 85, 83, 88, 89, 84]
    overall_data = [82, 84, 87, 84, 89, 90, 85]
    
    chart_data = pd.DataFrame({
        'Day': days,
        'Helmet': helmet_data,
        'Vest': vest_data,
        'Overall': overall_data
    })
    
    fig = px.line(chart_data, x='Day', y=['Helmet', 'Vest', 'Overall'], 
                  title='Weekly PPE Compliance Rates')
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent violations
    st.subheader("🚨 Recent Violations")
    
    # Create a DataFrame for violations
    violation_df = pd.DataFrame(sample_violations)
    st.dataframe(violation_df, use_container_width=True)
    
    # Compliance by zone
    st.subheader("📍 Compliance by Zone")
    
    zone_data = pd.DataFrame({
        'Zone': ['Zone A', 'Zone B', 'Zone C', 'Zone D'],
        'Compliance %': [85, 92, 78, 90]
    })
    
    fig2 = px.bar(zone_data, x='Zone', y='Compliance %', 
                  title='Compliance Rates by Work Zone',
                  color='Compliance %',
                  color_continuous_scale='viridis')
    st.plotly_chart(fig2, use_container_width=True)

# Real-time Monitoring Page
elif page == "Real-time Monitoring":
    st.header("🎥 Real-time Video Feed Analysis")
    
    # Simulated camera feeds
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Camera Feed 1 - Main Entrance")
        # Using a construction site image for demo
        st.image("https://i.imgur.com/2QxE3SR.jpeg", caption="Live Feed - Main Entrance", use_column_width=True)
        st.progress(85)
        st.caption("Occupancy: 12 people | Compliance: 85%")
        
    with col2:
        st.subheader("Camera Feed 2 - Workshop Area")
        # Using another construction site image for demo
        st.image("https://i.imgur.com/XNf5UdC.jpg", caption="Live Feed - Workshop Area", use_column_width=True)
        st.progress(78)
        st.caption("Occupancy: 18 people | Compliance: 78%")
    
    st.markdown("---")
    
    # Detected objects summary
    st.subheader("🔍 Current Detections")
    
    # Simulate detections
    detections = []
    for i in range(8):
        person_id = f"PERSON-{random.randint(100, 999)}"
        ppe_status = {}
        for ppe in ppe_classes:
            ppe_status[ppe] = random.choice([True, True, True, False])  # Weighted toward compliant
        
        detections.append({
            "Person ID": person_id,
            "Helmet": "✅" if ppe_status['Helmet'] else "❌",
            "Vest": "✅" if ppe_status['Vest'] else "❌",
            "Gloves": "✅" if ppe_status['Gloves'] else "❌",
            "Status": "Compliant" if all(ppe_status.values()) else "Non-Compliant"
        })
    
    detection_df = pd.DataFrame(detections)
    st.dataframe(detection_df.style.applymap(lambda x: 'background-color: #ffcccc' if x == '❌' else '', subset=['Helmet', 'Vest', 'Gloves']), 
                 use_container_width=True)
    
    # Alert panel
    st.subheader("⚠️ Active Alerts")
    
    alert_col1, alert_col2 = st.columns(2)
    
    with alert_col1:
        st.error("🚨 HIGH RISK: Person without helmet detected in Zone B")
        st.info("👤 Person ID: EMP-021")
        st.text("🕒 Time: 10:15 AM")
        
    with alert_col2:
        st.warning("⚠️ MEDIUM RISK: Person without vest detected in Zone A")
        st.info("👤 Person ID: EMP-008")
        st.text("🕒 Time: 10:08 AM")

# Violation Reports Page
elif page == "Violation Reports":
    st.header("📋 Violation Reports & Analytics")
    
    # Date selector
    date_range = st.date_input("Select Date Range", [])
    
    # Violation statistics
    st.subheader("📈 Violation Statistics")
    
    # Violation types chart
    violation_types = ['No Helmet', 'No Vest', 'No Gloves', 'No Boots', 'No Goggles']
    violation_counts = [25, 18, 12, 8, 5]
    
    violation_data = pd.DataFrame({
        'Type': violation_types,
        'Count': violation_counts
    })
    
    fig3 = px.pie(violation_data, values='Count', names='Type', 
                  title='Violations by PPE Type')
    st.plotly_chart(fig3, use_container_width=True)
    
    # Detailed violation log
    st.subheader("📖 Detailed Violation Log")
    
    # Expand the sample violations with more data
    detailed_violations = []
    for i in range(20):
        detailed_violations.append({
            'Timestamp': f"{random.randint(1, 12):02d}:{random.randint(0, 59):02d} {'AM' if random.random() > 0.5 else 'PM'}",
            'Location': f"Zone {random.choice(['A', 'B', 'C', 'D'])}",
            'Person ID': f"EMP-{random.randint(1, 999):03d}",
            'Violation Type': random.choice(violation_types),
            'Severity': random.choice(['High', 'Medium', 'Low']),
            'Action Taken': random.choice(['Notified Supervisor', 'Issued Warning', 'None'])
        })
    
    violation_log_df = pd.DataFrame(detailed_violations)
    st.dataframe(violation_log_df, use_container_width=True)
    
    # Export option
    st.download_button(
        label="📥 Download Report as CSV",
        data=violation_log_df.to_csv().encode('utf-8'),
        file_name="safetyeye_violations_report.csv",
        mime="text/csv"
    )

# Settings Page
elif page == "Settings":
    st.header("⚙️ System Settings")
    
    st.subheader("Camera Configuration")
    st.checkbox("Enable Camera Feed 1", value=True)
    st.checkbox("Enable Camera Feed 2", value=True)
    st.checkbox("Enable Camera Feed 3", value=False)
    st.checkbox("Enable Camera Feed 4", value=False)
    
    st.subheader("Alert Thresholds")
    st.slider("Minimum Compliance Threshold (%)", 0, 100, 80)
    st.selectbox("Alert Notification Method", ["Email", "SMS", "Both"])
    
    st.subheader("AI Model Configuration")
    st.selectbox("Model Version", ["v2.1 (Latest)", "v2.0", "v1.5"])
    st.checkbox("Enable Real-time Processing", value=True)
    st.checkbox("Enable Anomaly Detection", value=True)
    
    st.subheader("Data Retention")
    st.selectbox("Log Retention Period", ["30 days", "90 days", "1 year", "Indefinite"])
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")