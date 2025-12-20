import streamlit as st
import pandas as pd
from pathlib import Path
import base64


# ==========================================================
# LOAD VIOLATION DATA
# ==========================================================
def load_data():
    csv_path = Path("database/violations_log.csv")

    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return pd.DataFrame(columns=["id", "label", "confidence", "image", "timestamp"])

    try:
        df = pd.read_csv(
            csv_path,
            header=None,
            names=["id", "label", "confidence", "image", "timestamp"]
        )
        return df
    except:
        return pd.DataFrame(columns=["id", "label", "confidence", "image", "timestamp"])


# ==========================================================
# PDF VIEWER (BASE64 EMBED)
# ==========================================================
def embed_pdf_base64(file_path):
    try:
        with open(file_path, "rb") as pdf:
            base64_pdf = base64.b64encode(pdf.read()).decode("utf-8")

        return f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="350"
            style="border:1px solid #2a2f37; border-radius:8px;"
        ></iframe>
        """
    except:
        return None


# ==========================================================
# MAIN REPORTS PAGE
# ==========================================================
def app():
    st.subheader("📄 Violation Reports")

    df = load_data()

    if df.empty:
        st.info("⚠ No violation records found. Start Live Monitoring first.")
        return

    # Latest first
    df = df.sort_values("timestamp", ascending=False)

    # ---------------------- SEARCH BAR ----------------------
    search = st.text_input("🔍 Search by ID, Label or Date:")

    if search.strip():
        search = search.lower()
        df = df[df.apply(
            lambda row:
                search in str(row["id"]).lower() or
                search in str(row["label"]).lower() or
                search in str(row["timestamp"]).lower(),
            axis=1
        )]

    st.write(f"📌 Showing **{len(df)}** records")
    st.markdown("---")

    # ======================================================
    # RENDER EACH VIOLATION CARD (OLD STYLE YOU LIKED)
    # ======================================================
    for _, row in df.iterrows():

        with st.container():
            col1, col2 = st.columns([3, 2])

            # LEFT SIDE (INFO + IMAGE)
            with col1:
                st.markdown(f"### 🆔 {row['id']} — **{row['label']}**")
                st.write(f"📅 `{row['timestamp']}`")
                st.write(f"🎯 Confidence: **{row['confidence']:.2f}**")

                img_path = Path(row["image"])

                if img_path.exists():
                    st.image(str(img_path), width=350)
                else:
                    st.warning("❌ Image Missing")

            # RIGHT SIDE (PDF SECTION)
            with col2:
                pdf_path = Path(f"database/{row['id']}.pdf")

                if pdf_path.exists():

                    # Download button
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📥 Download PDF Challan",
                            data=f,
                            file_name=f"{row['id']}.pdf",
                            mime="application/pdf",
                            key=f"download_{row['id']}"
                        )

                    # Preview PDF
                    viewer = embed_pdf_base64(pdf_path)
                    if viewer:
                        st.markdown("#### 📘 PDF Preview", unsafe_allow_html=True)
                        st.markdown(viewer, unsafe_allow_html=True)
                    else:
                        st.warning("⚠ Unable to preview PDF")

                else:
                    st.warning("🚫 PDF not found for this violation.")

            st.markdown("---")
