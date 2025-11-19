import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(
    page_title="Safety Monitoring Dashboard",
    page_icon="🚦",
    layout="wide",
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
    <style>
    /* Background and text */
    body {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .main {
        background-color: #0E1117;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E1E;
        padding: 10px 20px;
        border-radius: 10px;
        color: #FAFAFA;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #31333F;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0072FF;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- TITLE -----------------
st.title("🚦 Real-Time Safety Monitoring Dashboard (Prototype)")
st.caption("Monitoring • Analytics • Logs — A smart safety visualization system")

# ----------------- SIDEBAR -----------------
st.sidebar.header("⚙️ Dashboard Controls")
st.sidebar.info("Prototype dashboard before YOLO integration. Real-time data will be added later.")
theme_choice = st.sidebar.selectbox("Theme Mode", ["Dark", "Light"])
refresh_rate = st.sidebar.slider("Auto-refresh (seconds)", 0, 30, 5)

# ----------------- TABS -----------------
tab1, tab2, tab3 = st.tabs(["📹 Live Feed", "📈 Analytics", "🧾 Logs"])

# ----------------- TAB 1: LIVE FEED -----------------
with tab1:
    st.subheader("🔴 Live Feed (Demo Preview)")
    st.markdown("This section will later display real-time video detection overlays from YOLOv8.")
    st.image("https://cdn.pixabay.com/photo/2016/11/29/05/30/road-1867041_1280.jpg",
             caption="Sample Surveillance Feed", use_container_width=True)
    st.button("▶ Start Stream", type="primary")

# ----------------- TAB 2: ANALYTICS -----------------
with tab2:
    st.subheader("📊 Violation Analytics")

    # Example dataset
    times = pd.date_range(datetime.datetime.now() - datetime.timedelta(hours=9), periods=10, freq="H")
    violations = [1, 0, 2, 1, 3, 2, 4, 1, 0, 3]
    df = pd.DataFrame({"Time": times, "Violations": violations})

    col1, col2 = st.columns(2)

    with col1:
        fig_line = px.line(df, x="Time", y="Violations",
                           title="Violations Over Time",
                           markers=True,
                           color_discrete_sequence=["#FF4B4B"])
        fig_line.update_layout(template="plotly_dark", plot_bgcolor="#0E1117", paper_bgcolor="#0E1117")
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        # Sample breakdown by type
        type_data = pd.DataFrame({
            "Violation Type": ["No Helmet", "Over Speed", "Signal Jump"],
            "Count": [12, 9, 5]
        })
        fig_pie = px.pie(type_data, names="Violation Type", values="Count",
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         title="Violation Type Distribution")
        fig_pie.update_layout(template="plotly_dark", plot_bgcolor="#0E1117", paper_bgcolor="#0E1117")
        st.plotly_chart(fig_pie, use_container_width=True)

# ----------------- TAB 3: LOGS -----------------
with tab3:
    st.subheader("🧾 Violation Logs")
    logs = pd.DataFrame({
        "Time": ["2025-11-13 10:00", "2025-11-13 11:30", "2025-11-13 14:20", "2025-11-13 16:10"],
        "Type": ["No Helmet", "Over Speed", "Signal Jump", "No Helmet"],
        "Confidence": [0.91, 0.84, 0.89, 0.93],
        "Location": ["Camera 1", "Camera 3", "Camera 2", "Camera 1"]
    })
    st.dataframe(logs, use_container_width=True, height=250)
    st.caption("✅ Logs displayed successfully (sample data).")

# ----------------- FOOTER -----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<center>Developed by <b>Sanmaya I K</b> | Prototype Dashboard © 2025</center>",
    unsafe_allow_html=True
)
