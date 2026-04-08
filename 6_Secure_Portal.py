import streamlit as st

if "authenticated" not in st.session_state:
    st.error("Unauthorized access")
    st.stop()

st.title("📁 Secure Portal")

st.write("This area represents protected system resources.")

st.info("""
Example Protected Resources:

• Confidential company documents  
• Research datasets  
• Employee records  
• Security reports
""")

st.success("Access granted to secure resources.")

if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")
