import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>
        :root { --bg:#eef8ff; --sidebar:#0b1220; --card:#ffffff; --muted:#6b7280; --accent:#0f172a; --primary:#2563eb; --success:#10b981; }
        body, .stApp { font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; color: var(--accent); background: linear-gradient(180deg, var(--bg) 0%, #ffffff 100%); }
        /* Sidebar */
        .css-1lcbmhc.e1fqkh3o1 { background: var(--sidebar) !important; }
        .stSidebar .stButton>button { background: transparent; border: 1px solid rgba(255,255,255,0.06); color: #e6eef8; }

        /* Cards and layout */
        .card { background: var(--card); padding: 16px; border-radius: 12px; box-shadow: 0 10px 30px rgba(2,6,23,0.06); margin-bottom: 16px; }
        .kpi { font-size:22px; font-weight:700; color:#0f172a; }
        .kpi-sub { font-size:13px; color:var(--muted); }
        .zone-title { font-weight:700; color:#0f172a; margin:8px 0 12px 0; }
        .avatar-card { display:inline-block; background: transparent; padding:6px; border-radius:8px; }
        .zone-row { padding:12px 8px; border-radius:10px; background:linear-gradient(180deg,#ffffff,#fbfdff); }
        .controls { padding:12px; }
        .alert-success { background: #ecfdf5; border:1px solid #bbf7d0; color:#065f46; padding:10px; border-radius:8px; }
        .alert-danger { background:#fff1f2; border:1px solid #fecaca; color:#7f1d1d; padding:10px; border-radius:8px; }
        .section-gap { height:12px; }
        /* Refresh area style (main panel) */
        .refresh-area { background: linear-gradient(90deg, rgba(37,99,235,0.06), rgba(16,185,129,0.04)); padding:10px; border-radius:10px; display:inline-block; }
        .sim-controls { background: linear-gradient(180deg,#ffffff,#f3fbff); padding:10px; border-radius:10px; }
        .landing { background: linear-gradient(90deg,#e6f7ff 0%, #ffffff 100%); }
        </style>
        """,
        unsafe_allow_html=True,
    )
