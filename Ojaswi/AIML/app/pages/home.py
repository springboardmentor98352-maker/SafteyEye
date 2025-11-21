import streamlit as st
from datetime import datetime
import random

def app():
    st.markdown('<div class="hero"><h1 style="margin:0">🪐 SafetyEye — Overview</h1><div class="small-muted">Purple Galaxy theme • Live PPE monitoring</div></div>', unsafe_allow_html=True)
    st.write('')

    # KPI row
    c1, c2, c3, c4 = st.columns([1.1,1,1,1])
    c1.markdown('<div class="card"><div class="kpi"><div><span class="num">32</span></div><div style="margin-left:8px"><div class="lbl">Total Violations</div><div class="small-muted">+3 today</div></div></div></div>', unsafe_allow_html=True)
    c2.markdown('<div class="card"><div class="kpi"><div><span class="num">89%</span></div><div style="margin-left:8px"><div class="lbl">Helmet Compliance</div><div class="small-muted">+2%</div></div></div></div>', unsafe_allow_html=True)
    c3.markdown('<div class="card"><div class="kpi"><div><span class="num">93%</span></div><div style="margin-left:8px"><div class="lbl">Mask Compliance</div><div class="small-muted">+1%</div></div></div></div>', unsafe_allow_html=True)
    c4.markdown('<div class="card"><div class="kpi"><div><span class="num">3</span></div><div style="margin-left:8px"><div class="lbl">Active Cameras</div><div class="small-muted">Online</div></div></div></div>', unsafe_allow_html=True)

    st.markdown('---')
    st.subheader('Recent Violations')

    cols = st.columns(3)
    rows = []

    for i in range(6):
        rows.append({
            'id': i+1,
            'label': random.choice(['NO-Hardhat','NO-Vest','NO-Mask']),
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    for idx, r in enumerate(rows):
        c = cols[idx % 3]
        c.markdown(
            f"""
            <div class='card'>
                <b>ID:</b> {r['id']}<br>
                <b>Type:</b> {r['label']}<br>
                <span class='small-muted'>{r['time']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="footer">Tip: Connect backend at <code>http://localhost:8000</code> to enable live data and logs.</div>', unsafe_allow_html=True)
