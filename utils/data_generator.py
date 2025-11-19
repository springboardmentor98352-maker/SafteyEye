import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st




def generate_mock_data():
# Use session state settings if available
zones = st.session_state.get('zones', ["Assembly Line A"]) or ["Assembly Line A"]
max_occupancy = st.session_state.get('max_occupancy', 50)


current_time = datetime.now()


occupancy_data = {
'zone': zones,
'current': list(np.random.randint(10, max_occupancy, len(zones))),
'max_capacity': [max_occupancy] * len(zones),
'helmet_compliance': list(np.random.randint(75, 100, len(zones))),
'vest_compliance': list(np.random.randint(70, 100, len(zones)))
}


hours = [(current_time - timedelta(hours=x)).strftime('%H:%M') for x in range(24, 0, -1)]
historical_data = pd.DataFrame({
'time': hours,
'occupancy': np.random.randint(20, 80, 24),
'compliance': np.random.randint(75, 100, 24),
'violations': np.random.randint(0, 5, 24)
})


return occupancy_data, historical_data