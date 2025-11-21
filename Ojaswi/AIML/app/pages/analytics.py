import streamlit as st
import pandas as pd
import altair as alt
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap

def app():
    st.markdown("<h1 style='color:#ff4d4d;'>📊 Traffic Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.write("Real-time insights, violation trends, hotspot heatmaps & zone intelligence.")

    # -----------------------------
    #  SAMPLE DATA (Replace with backend later)
    # -----------------------------
    data = pd.DataFrame({
        "zone": ["A", "B", "C", "A", "C", "B", "A"],
        "type": ["NO-Helmet", "Speeding", "Triple Riding", "Signal Jump", "NO-Seatbelt", "Speeding", "NO-Helmet"],
        "count": [23, 40, 12, 18, 30, 29, 25],
        "lat": [19.0760, 19.0910, 19.0650, 19.0801, 19.1103, 19.0402, 19.0988],
        "lon": [72.8777, 72.8890, 72.8700, 72.8992, 72.8601, 72.8400, 72.9155],
    })

    # -----------------------------
    # 1. VIOLATION TREND (ALT-AIR)
    # -----------------------------
    st.subheader("📈 Violations Trend Over Time")

    chart = (
        alt.Chart(data)
        .mark_bar(color="#ff4d4d")
        .encode(
            x="type:N",
            y="count:Q",
            tooltip=["type", "count"]
        )
        .properties(height=350)
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # 2. ZONE-WISE PIE CHART
    # -----------------------------
    st.subheader("🗂️ Zone-Wise Violations")

    zone_df = data.groupby("zone")["count"].sum().reset_index()

    pie = (
        alt.Chart(zone_df)
        .mark_arc()
        .encode(
            theta="count:Q",
            color="zone:N",
            tooltip=["zone", "count"]
        )
    )
    st.altair_chart(pie, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # 3. VIOLATION HOTSPOT MAP (FOLIUM)
    # -----------------------------
    st.subheader("🔥 Violation Hotspot Heatmap (Mumbai)")

    m = folium.Map(location=[19.0760, 72.8777], zoom_start=12, tiles="CartoDB dark_matter")

    # Add heatmap
    HeatMap(data[["lat", "lon"]].values.tolist(), radius=15).add_to(m)

    # Add marker for each violation
    for _, row in data.iterrows():
        folium.Marker(
            [row["lat"], row["lon"]],
            tooltip=f"{row['type']} ({row['count']})",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

    st_folium(m, height=500, width=700)

    st.markdown("---")

    # -----------------------------
    # 4. TRAFFIC POLICE NOTES PANEL
    # -----------------------------
    st.subheader("📝 Officer Notes")
    note = st.text_area("Field officer summary", height=120)
    if st.button("Save Note"):
        st.success("Note saved successfully (local mode).")

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Connect backend → to fetch real traffic logs, violation clusters & maps.")
