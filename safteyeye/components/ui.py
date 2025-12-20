import streamlit as st
import textwrap
from datetime import datetime

def set_global_styles():
    # modern palette, subtle card shadow and fonts
    st.markdown(
        """
        <style>
        /* layout */
        .stApp { background: linear-gradient(90deg,#0f1720 0%, #071026 100%); color: #e6eef8; }
        .stSidebar { background: #0b1220; color:#dbe7ff; padding-top:18px; }
        /* cards */
        .card { background: linear-gradient(180deg,#0f1728 0%, #07101a 100%); border-radius:12px;
                padding:16px; box-shadow: 0 6px 18px rgba(3,10,20,0.6); border:1px solid rgba(255,255,255,0.03); }
        .kpi { font-size:20px; font-weight:700; color:#ffffff; }
        .kpi-sub { color:#9fb0d7; font-size:12px; }
        /* small badges */
        .badge { display:inline-block; padding:4px 8px; border-radius:999px; font-size:12px; }
        .badge-green { background: rgba(56,189,248,0.09); color:#38bdf8; border:1px solid rgba(56,189,248,0.12); }
        .badge-red { background: rgba(248,113,113,0.08); color:#f87171; border:1px solid rgba(248,113,113,0.12); }
        /* AI assistant style */
        .ai-box { background: linear-gradient(180deg,#07112a, #041023); border-radius:12px; padding:12px; margin-top:8px; border:1px solid rgba(255,255,255,0.03);}
        .ai-title { font-weight:700; color:#dbe7ff; }
        .muted { color:#9fb0d7; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _format_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sidebar_control_panel():
    """Return a state dict used by pages. Keeps keys stable: 'zones', 'max_capacity', etc."""
    if "monitoring" not in st.session_state:
        st.session_state.monitoring = False

    with st.sidebar:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Control Panel")
        if st.button("🟢 Start Monitoring" if not st.session_state.monitoring else "🔴 Stop Monitoring"):
            st.session_state.monitoring = not st.session_state.monitoring

        st.markdown("---")
        st.markdown("**📍 Zones**")
        zones = st.multiselect(
            "Select zones to monitor",
            [
                "Assembly Line A", "Assembly Line B", "Warehouse", "Loading Dock",
                "Office Floor 1", "Office Floor 2", "Cafeteria", "Parking Area"
            ],
            default=["Assembly Line A", "Warehouse"]
        )

        st.markdown("**🛡️ Safety Thresholds**")
        helmet_threshold = st.slider("Helmet compliance (%)", 0, 100, 90)
        vest_threshold = st.slider("Vest compliance (%)", 0, 100, 85)
        max_capacity = st.number_input("Max occupancy per zone", min_value=5, max_value=200, value=50)

        st.markdown("---")
        st.markdown("**🔔 Alerts**")
        alert_email = st.checkbox("Email Alerts", value=True)
        alert_sound = st.checkbox("Sound Alerts", value=False)

        st.markdown("---")
        st.markdown("<div class='muted'>Updated:</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='muted'>{_format_time()}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Small AI assistant box
        st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
        st.markdown("<div class='ai-title'>Assistant — Quick Insights</div>", unsafe_allow_html=True)
        # mock insights (generated from chosen controls); keep simple deterministic text
        if not zones:
            st.markdown("<div class='muted'>No zones selected — choose zones to enable live insights.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='margin-top:8px'>Monitoring <strong>{len(zones)}</strong> zones. Recommended action:</div>", unsafe_allow_html=True)
            # simple heuristics for mock suggestions
            suggestions = []
            if helmet_threshold < 85:
                suggestions.append("Raise helmet compliance threshold to >= 85% for industrial zones.")
            if max_capacity > 100:
                suggestions.append("Split large zones into subzones to improve tracking fidelity.")
            if alert_email:
                suggestions.append("Email alerts enabled — configure SMTP in backend for real notifications.")
            if not suggestions:
                suggestions.append("All basic settings look good. Run live demo and check analytics.")
            for s in suggestions[:3]:
                st.markdown(f"- {s}")
        st.markdown("</div>", unsafe_allow_html=True)

    if not zones:
        zones = ["Assembly Line A"]
    return {
        "monitoring_active": st.session_state.monitoring,
        "zones": zones,
        "helmet_threshold": helmet_threshold,
        "vest_threshold": vest_threshold,
        "max_capacity": int(max_capacity),
        "alert_email": alert_email,
        "alert_sound": alert_sound
    }
