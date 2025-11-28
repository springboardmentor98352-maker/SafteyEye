import streamlit as st
from data import mock_data
import plotly.graph_objects as go
import plotly.express as px

def app(state):
    st.subheader("📈 Analytics")

    hist = mock_data.gen_history()

    # user-controlled smoothing / hours
    hours_select = st.select_slider("Hours window", options=list(range(6,25)), value=24)
    hist_sub = hist.tail(hours_select)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist_sub["time"], y=hist_sub["occupancy"], mode="lines+markers", name="Occupancy", line=dict(width=3)))
    fig.update_layout(title=f"Last {hours_select} hours — Occupancy", xaxis_title="Time", yaxis_title="Count", height=380)
    st.plotly_chart(fig, width="stretch")

    st.divider()
    st.subheader("Violations (recent)")
    fig2 = px.bar(hist_sub, x="time", y="violations", title="Violations", color="violations")
    st.plotly_chart(fig2, width="stretch")
