import streamlit as st
import pandas as pd
from pathlib import Path

def load_data():
    csv_path = Path("database/violations_log.csv")
    if not csv_path.exists():
        return pd.DataFrame(columns=["id","label","confidence","image","timestamp"])
    return pd.read_csv(csv_path, header=None, names=["id","label","confidence","image","timestamp"])


def app():
    st.subheader("📄 Violation Records")

    df = load_data()

    if df.empty:
        st.info("⚠ No records found. Start Live Monitoring first.")
        return

    df = df.sort_values("timestamp", ascending=False)

    # ======= SEARCH BAR =======
    search = st.text_input("🔍 Search by Violation Type, ID or Timestamp:", "")

    if search.strip():
        df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)]

    st.write(f"📌 Showing **{len(df)}** records")

    # ======= EXPORT BUTTON =======
    export_df = df.copy()
    export_df.to_csv("database/exported_violations.csv", index=False)

    st.download_button(
        label="📤 Download CSV (Filtered Results)",
        data=export_df.to_csv(index=False),
        file_name="SafetyEye_Report.csv",
        mime="text/csv"
    )

    st.markdown("---")


    # ======= LIST DISPLAY =======
    for idx, row in df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 2])

            # Left Section
            with col1:
                st.write(f"### 🆔 {row['id']} — {row['label']}")
                st.write(f"📅 {row['timestamp']}")
                st.write(f"🎯 Confidence: **{row['confidence']:.2f}**")

                image_path = Path(row["image"])
                if image_path.exists():
                    st.image(str(image_path), width=350)
                else:
                    st.warning("❌ Image missing")

            # Right Section
            with col2:
                pdf_path = Path(f"database/{row['id']}.pdf")

                if pdf_path.exists():
                    # Download button
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Challan PDF",
                            data=f,
                            file_name=f"{row['id']}.pdf",
                        )

                    # Preview
                    st.markdown(f"📎 **Preview:** `{row['id']}.pdf`")
                    st.markdown(
                        f'<iframe src="database/{row["id"]}.pdf" width="100%" height="300"></iframe>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.warning("🚫 PDF missing")
