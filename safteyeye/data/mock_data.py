import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def gen_occupancy(zones, max_capacity=50):
    if not zones:
        zones = ["Assembly Line A"]
    current = [int(np.random.randint(1, max_capacity+1)) for _ in zones]
    helmet = [int(np.random.randint(60, 100)) for _ in zones]
    vest = [int(np.random.randint(60, 100)) for _ in zones]
    return {
        "zone": zones,
        "current": current,
        "max_capacity": [max_capacity for _ in zones],
        "helmet_compliance": helmet,
        "vest_compliance": vest
    }

def gen_history():
    now = datetime.now()
    hours = [(now - timedelta(hours=i)).strftime("%H:%M") for i in range(23, -1, -1)]
    df = pd.DataFrame({
        "time": hours,
        "occupancy": np.random.randint(10, 100, size=24),
        "compliance": np.random.randint(60, 100, size=24),
        "violations": np.random.randint(0, 6, size=24)
    })
    return df
