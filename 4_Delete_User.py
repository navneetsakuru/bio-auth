import streamlit as st

st.set_page_config(page_title="Biometric Authentication System", layout="wide")

st.markdown("""
<style>

/* Main app background */
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
}

/* Titles */
h1,h2,h3 {
    color:#38bdf8;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#2563eb,#06b6d4);
    color:white;
    border-radius:8px;
    height:45px;
    font-size:16px;
    border:none;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background:#1e293b;
    padding:10px;
    border-radius:8px;
}

/* Info boxes */
.stAlert {
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)




import streamlit as st
import os
import shutil
st.set_page_config(page_title="Biometric Authentication System", layout="wide")

st.markdown("""
<style>

/* Entire background */
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color: white;
}

/* Titles */
h1,h2,h3 {
    color: #38bdf8;
}

/* Paragraph text */
p, label, span {
    color: #e2e8f0;
    font-size: 16px;
}

/* Buttons */
.stButton>button {
    background: #3b82f6;
    color: white;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background: #2563eb;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #334155;
    padding: 12px;
    border-radius: 10px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #1e293b;
    padding: 15px;
    border-radius: 10px;
}

/* Cards / containers */
.block-container {
    padding-top: 2rem;
}

/* Alerts */
.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

TEMPLATE_DIR = "templates"

if "authenticated" not in st.session_state:
    st.error("Unauthorized access")
    st.stop()

st.title("Delete User")

users = os.listdir(TEMPLATE_DIR)

selected = st.selectbox("Select user", users)

confirm = st.checkbox("Confirm deletion")

if st.button("Delete User"):

    if confirm:

        user_dir = os.path.join(TEMPLATE_DIR, selected)

        shutil.rmtree(user_dir)

        st.success("User deleted")

    else:
        st.warning("Please confirm deletion")
