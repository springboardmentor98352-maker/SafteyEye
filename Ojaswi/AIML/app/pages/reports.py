# app/pages/reports.py
import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime
import time


def make_challan(record):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, "Traffic Violation Challan", ln=True, align='C')
    pdf.ln(6)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Case ID: {record.get('case_id', '')}", ln=True)
    pdf.cell(0, 8, f"Type: {record.get('label','')}", ln=True)
    pdf.cell(0, 8, f"Location: {record.get('location','')}", ln=True)
    pdf.cell(0, 8, f"Phone: {record.get('phone','')}", ln=True)
    pdf.cell(0, 8, f"Detected at: {record.get('timestamp','')}", ln=True)
    fname = f"challan_{record.get('case_id', str(int(time.time())))}.pdf"
    pdf.output(fname)
    return fname

def app():
    st.header("📑 Violations & Challan Generator")
    uploaded = st.file_uploader("Upload violations CSV (optional)", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df_path = os.path.join("..", "database", "violations_log.csv")
        if os.path.exists(df_path):
            df = pd.read_csv(df_path)
        else:
            df = pd.DataFrame(columns=['id','label','confidence','image_path','timestamp','location','phone'])
    st.dataframe(df)

    st.markdown("---")
    st.subheader("Create Challan (manual)")
    col1, col2 = st.columns(2)
    label = col1.selectbox("Violation Type", ["NO-Helmet","NO-Mask","NO-Vest","Overspeed","Signal Jump"])
    phone = col2.text_input("Phone number")
    location = col1.text_input("Location / Area")
    notes = col2.text_area("Notes")
    if st.button("Generate Challan PDF"):
        rec = {
            "case_id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "label": label,
            "location": location,
            "phone": phone,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "notes": notes
        }
        fname = make_challan(rec)
        with open(fname, "rb") as f:
            st.download_button("Download Challan", f, file_name=fname)
        st.success("Challan generated and ready to download.")
