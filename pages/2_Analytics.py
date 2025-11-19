import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.data_generator import generate_mock_data
from components.theme import inject_theme


inject_theme()


st.title("📈 Analytics")


occupancy_data, historical_data = generate_mock_data()


col1, col2 = st.columns(2)
with col1:
fig_occupancy = go.Figure()
fig_occupancy.add_trace(go.Scatter(
x=historical_data['time'], y=historical_data['occupancy'], mode='lines+markers', name='Occupancy', fill='tozeroy'
))
fig_occupancy.update_layout(title="24-Hour Occupancy Trend", height=350)
st.plotly_chart(fig_occupancy, use_container_width=True)


fig_compliance = px.bar(
px.data.tips() # placeholder to ensure a chart renders if df empty
)


with col2:
fig_compliance_trend = go.Figure()
fig_compliance_trend.add_trace(go.Scatter(x=historical_data['time'], y=historical_data['compliance'], mode='lines+markers', name='Compliance'))
fig_compliance_trend.add_hline(y=90, line_dash='dash', line_color='red', annotation_text='Target: 90%')
fig_compliance_trend.update_layout(title='24-Hour Safety Compliance Trend', height=350)
st.plotly_chart(fig_compliance_trend, use_container_width=True)


st.subheader("Zone Utilization Heatmap")
zones = occupancy_data['zone']
heatmap_data = np.random.randint(0, 100, size=(len(zones), 24))
fig_heatmap = go.Figure(data=go.Heatmap(z=heatmap_data, x=historical_data['time'], y=zones, colorscale='RdYlGn'))
fig_heatmap.update_layout(title='Zone Utilization % (24 Hours)', height=400)
st.plotly_chart(fig_heatmap, use_container_width=True)