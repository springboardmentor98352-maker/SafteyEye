import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime

from style_utils import apply_global_styles
from data_utils import make_sample, safe_load_uploaded_csv, default_thresholds, generate_violations
from avatar_utils import make_flat_avatar
from simulator import create_worker_scene, init_sim_state


def show_dashboard(go):
    apply_global_styles()

    # Header
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.title("👁️‍🗨️ SafetyEye — Occupancy & Safety Monitor (MVP)")
        st.markdown("_Demo dashboard using simulated logs or uploaded CSV. No model needed._")
    with col2:
        st.image("https://raw.githubusercontent.com/ultralytics/assets/main/ultralytics-logo.svg", width=100)

    st.divider()

    # Sidebar inputs
    st.sidebar.header("Controls & Inputs")
    mode = st.sidebar.radio("Mode", ["Simulated Stream", "Upload CSV / Logs", "Single Image (preview)"])

    st.sidebar.subheader("Zone Thresholds (people)")
    thresholds = default_thresholds()
    for z in list(thresholds.keys()):
        thresholds[z] = st.sidebar.number_input(f"Threshold — {z}", min_value=1, value=thresholds[z], step=1)

    layout_img = st.sidebar.file_uploader("Optional: Upload floor plan / zone map", type=["png","jpg","jpeg"])
    use_model = st.sidebar.checkbox("Enable CV model (placeholder)", value=False)
    if use_model:
        st.sidebar.info("This is a placeholder. No model is required to run this demo.")

    # Avatar / people view controls
    st.sidebar.markdown("---")
    avatar_style = st.sidebar.selectbox("Person style", ["Stylized Icons", "Generated Avatars (more realistic)", "Photo thumbnails (upload)"], index=1)
    avatar_size = st.sidebar.slider("Avatar size", min_value=48, max_value=160, value=96, step=8)
    per_row_default = 8
    per_row = st.sidebar.number_input("Avatars per row", min_value=3, max_value=12, value=per_row_default)
    upload_people = None
    if avatar_style == "Photo thumbnails (upload)":
        upload_people = st.sidebar.file_uploader("Upload person images (multiple)", accept_multiple_files=True, type=["png","jpg","jpeg"])

    st.sidebar.markdown("---")
    st.sidebar.markdown("Download a sample CSV to test upload:")
    sample_df = make_sample(180)
    sample_csv_bytes = sample_df.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button("Download sample CSV", data=sample_csv_bytes, file_name="sample_occupancy.csv", mime="text/csv")

    # ---- Load Data ----
    if mode == "Upload CSV / Logs":
        uploaded = st.file_uploader("Upload CSV (timestamp, zone, people_count)", type=["csv"])
        if uploaded:
            df = safe_load_uploaded_csv(uploaded)
            if not {'timestamp', 'zone', 'people_count'}.issubset(df.columns):
                st.error("CSV must contain columns: timestamp, zone, people_count")
                df = pd.DataFrame(columns=['timestamp', 'zone', 'people_count'])
        else:
            st.info("No file uploaded — using sample data.")
            df = sample_df.copy()
    elif mode == "Single Image (preview)":
        uploaded_img = st.file_uploader("Upload an image (preview only)", type=["png","jpg","jpeg"])
        if uploaded_img:
            try:
                img = Image.open(uploaded_img)
                st.image(img, caption="Preview image", use_column_width=True)
            except Exception as e:
                st.warning("Could not open image: " + str(e))
        df = make_sample(60)
    else:
        df = sample_df.copy()

    # Clean / enforce types
    if not df.empty:
        if 'timestamp' in df.columns:
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            except Exception:
                pass
        if 'people_count' in df.columns:
            df['people_count'] = pd.to_numeric(df['people_count'], errors='coerce').fillna(0).astype(int)
        else:
            df['people_count'] = 0
    else:
        df = pd.DataFrame(columns=['timestamp', 'zone', 'people_count'])

    # Zone selection
    zones = sorted(df['zone'].dropna().unique().tolist())
    selected_zones = st.multiselect("Zones to display", options=zones, default=zones if zones else [])
    if selected_zones:
        df = df[df['zone'].isin(selected_zones)].sort_values('timestamp')
    else:
        df = df.sort_values('timestamp')

    # ---- Main layout ----
    left, right = st.columns([2, 1])

    with left:
        # KPIs
        k1, k2, k3 = st.columns(3)
        if not df.empty:
            latest = df.groupby('zone')['people_count'].last()
        else:
            latest = pd.Series(dtype='int64')

        total_people = int(latest.sum()) if not latest.empty else 0
        thresholds_series = pd.Series(thresholds).reindex(latest.index).fillna(999).astype(int) if not latest.empty else pd.Series(dtype='int64')
        total_violations = int((latest >= thresholds_series).sum()) if not latest.empty else 0
        compliance_rate = 100.0 if latest.empty else max(0.0, 100.0 - (total_violations / len(latest) * 100.0))

        with k1:
            st.markdown(f'<div class="card"><div class="kpi">{total_people} <span class="small">people now</span></div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="card"><div class="kpi">{total_violations} <span class="small">zones over limit</span></div></div>', unsafe_allow_html=True)
        with k3:
            st.markdown(f'<div class="card"><div class="kpi">{compliance_rate:.0f}% <span class="small">compliance</span></div></div>', unsafe_allow_html=True)

        st.markdown("### Occupancy — People View")

        if not latest.empty:
            color_palette = [
                (37,99,235), # blue
                (16,185,129), # green
                (234,88,12),  # orange
                (244,63,94),  # pink/red
                (99,102,241), # indigo
                (14,165,233), # cyan
            ]

            for zone in latest.index:
                cnt = int(latest[zone]) if zone in latest.index else 0
                with st.container():
                    st.markdown(f"<div class='zone-title'>{zone} — {cnt} people</div>", unsafe_allow_html=True)
                    if cnt <= 0:
                        st.write("No people detected in this zone.")
                        continue

                    avatars = []
                    for i in range(cnt):
                        if avatar_style == "Photo thumbnails (upload)" and upload_people:
                            f = upload_people[i % len(upload_people)]
                            try:
                                im = Image.open(f).convert('RGBA').resize((avatar_size, avatar_size))
                            except Exception:
                                im = make_flat_avatar(size=avatar_size, fill_color=color_palette[i % len(color_palette)])
                        else:
                            im = make_flat_avatar(size=avatar_size, fill_color=color_palette[i % len(color_palette)])
                        avatars.append(im)

                    for i in range(0, len(avatars), per_row):
                        row = avatars[i:i+per_row]
                        cols = st.columns(len(row))
                        for c, im in zip(cols, row):
                            c.image(im, width=avatar_size)
        else:
            st.info("No timeline / occupancy data available.")

        st.markdown("### Latest Zone Snapshot")
        if not latest.empty:
            snap = latest.reset_index().rename(columns={'people_count':'current_count'})
            snap['threshold'] = snap['zone'].map(thresholds).fillna(999).astype(int)
            snap['status'] = np.where(snap['current_count'] >= snap['threshold'], 'OVER LIMIT', 'OK')
            st.table(snap)
        else:
            st.info("No zone snapshot available (no data).")

        st.markdown("### Violation Log")
        violations_df = generate_violations(df, thresholds)
        if not violations_df.empty:
            st.dataframe(violations_df)
        else:
            st.info("No active violations detected.")

    with right:
        if st.button('← Home', key='back_home'):
            go('home')
        st.markdown("### Live Monitor")
        if layout_img:
            try:
                img = Image.open(layout_img)
                st.image(img, caption='Floor plan / zone map', use_column_width=True)
            except Exception:
                st.warning('Could not open layout image')

        st.markdown("### Controls")
        st.markdown('<div class="refresh-area">', unsafe_allow_html=True)
        if st.button("▶️ Refresh / Rerun", key='refresh_main'):
            pass
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Alerts")
        if not violations_df.empty:
            for _, r in violations_df.iterrows():
                st.error(f"{r['timestamp']} — {r['zone']}: {r['message']}")
        else:
            st.success("All zones within thresholds ✅")

        st.markdown("### Quick Actions")
        if not violations_df.empty:
            csv_bytes = violations_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download violation log CSV", data=csv_bytes, file_name="violations.csv", mime="text/csv")
        else:
            st.button("No violations to export", disabled=True)

    st.divider()
    st.markdown("**Notes:** This is an MVP dashboard that uses simulated logs or uploaded CSV. To add a CV model later, create an inference function and fill the placeholder `use_model` branch.")

    # ---- Worker Scene Simulator UI ----
    st.markdown("---")
    sim_enabled = st.checkbox("Enable worker scene simulator (preview)")
    if sim_enabled:
        init_sim_state()
        sim_show_ann = st.checkbox("Show annotations (labels & colours)", value=True)
        sim_bg = st.color_picker("Simulator background color", value="#f5f7fa")
        c1, c2, c3 = st.columns([1,1,2])
        st.markdown('<div class="sim-controls">', unsafe_allow_html=True)
        with c1:
            if st.button("Generate Scene"):
                img, cnt = create_worker_scene(show_annotations=sim_show_ann, bg_color=sim_bg)
                st.image(img, caption=f"Simulated scene — {cnt} workers", use_column_width=True)
        with c2:
            if st.button("Clear simulator logs"):
                st.session_state['sim_logs'] = []
                st.session_state['sim_total'] = 0
                st.success("Simulator logs cleared")
        with c3:
            st.metric("Total recorded violations", st.session_state.get('sim_total', 0))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### Recent Simulator Logs")
        if st.session_state['sim_logs']:
            st.dataframe(pd.DataFrame(st.session_state['sim_logs']).sort_values('time', ascending=False).reset_index(drop=True))
        else:
            st.info("No simulator logs yet. Click 'Generate Scene' to produce activity.")
