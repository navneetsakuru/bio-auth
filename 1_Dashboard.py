import streamlit as st
import pandas as pd
import os

if "authenticated" not in st.session_state:
    st.error("Unauthorized access")
    st.stop()

st.title("🔐 Security Dashboard")

st.write(f"Welcome **{st.session_state['user']}**")

st.divider()

col1,col2=st.columns(2)

with col1:

    if st.button("📁 Secure Portal",use_container_width=True):
        st.switch_page("pages/6_Secure_Portal.py")

    if st.button("📝 Enroll User",use_container_width=True):
        st.switch_page("pages/3_Enroll_User.py")

with col2:

    if st.button("🗑 Delete User",use_container_width=True):
        st.switch_page("pages/4_Delete_User.py")

    if st.button("📊 Authentication Logs",use_container_width=True):
        st.switch_page("pages/5_Authentication_Logs.py")

st.divider()


    
if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("streamlit_app.py")
