import streamlit as st

st.set_page_config(page_title="Biometric Security System", layout="wide")

st.markdown("""
<style>
.stApp{
background:linear-gradient(135deg,#0f172a,#1e293b);
color:white;
}

h1,h2,h3{
color:#38bdf8;
}

.stButton>button{
background:#2563eb;
color:white;
border-radius:10px;
height:50px;
font-size:18px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)


st.title("🔐 Multimodal Biometric Security System")

st.write("Secure authentication using **Fingerprint + Iris Biometrics**")

st.divider()



st.write("Click below to begin biometric authentication.")

if st.button("ACCESS PORTAL", use_container_width=True):
    st.switch_page("pages/2_Access_portal.py")
