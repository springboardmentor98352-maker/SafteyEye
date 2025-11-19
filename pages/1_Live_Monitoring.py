import streamlit as st
import pandas as pd
from utils.data_generator import generate_mock_data
from components.theme import inject_theme


inject_theme()


st.title("🎥 Live Monitoring")


occupancy_data, _ = generate_mock_data()


cols_per_row = 3
selected_zones = occupancy_data['zone']


for i in range(0, len(selected_zones), cols_per_row):
cols = st.columns(cols_per_row)
for j, col in enumerate(cols):
if i + j < len(selected_zones):
zone_name = selected_zones[i + j]
with col:
st.markdown(f"**📹 {zone_name}**")
st.image(f"https://via.placeholder.com/400x300/2c3e50/ffffff?text={zone_name.replace(' ', '+')}", use_container_width=True)
occupancy = occupancy_data['current'][i + j]
capacity = occupancy_data['max_capacity'][i + j]
helmet = occupancy_data['helmet_compliance'][i + j]
vest = occupancy_data['vest_compliance'][i + j]


col_a, col_b = st.columns(2)
with col_a:
st.metric("Occupancy", f"{occupancy}/{capacity}")
with col_b:
compliance = (helmet + vest) / 2
color = "🟢" if compliance >= 90 else "🟡" if compliance >= 80 else "🔴"
st.metric("Safety", f"{color} {int(compliance)}%")


st.divider()


st.subheader("Zone Details")
df_zones = pd.DataFrame(occupancy_data)
df_zones['utilization'] = (df_zones['current'] / df_zones['max_capacity'] * 100).round(1)
df_zones['overall_compliance'] = ((df_zones['helmet_compliance'] + df_zones['vest_compliance']) / 2).round(1)


st.dataframe(df_zones, use_container_width=True, hide_index=True)