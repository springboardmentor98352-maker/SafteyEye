import streamlit as st

def navbar():
    st.markdown(
        """
        <style>
            .navbar {
                background-color:#151515;
                padding:15px;
                border-radius:10px;
                margin-bottom:20px;
            }
            .navbar h2 { color:#ffffff; text-align:center; margin:0; }
        </style>
        <div class="navbar">
            <h2>SafetyEye 🚧</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
