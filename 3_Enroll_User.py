import streamlit as st
import numpy as np
import os
from PIL import Image
from training.feature_extractor import extract_features

if "authenticated" not in st.session_state:
    st.error("Unauthorized access")
    st.stop()

st.title("📝 Enroll New User")

person_name=st.text_input("Enter User ID")

col1,col2=st.columns(2)

with col1:
    fp_files=st.file_uploader("Upload Fingerprint Images",accept_multiple_files=True)

with col2:
    ir_files=st.file_uploader("Upload Iris Images",accept_multiple_files=True)


if st.button("Enroll User"):

    if not person_name or not fp_files or not ir_files:
        st.warning("Provide all inputs")
        st.stop()

    user_dir=os.path.join("templates",person_name)

    if os.path.exists(user_dir):
        st.error("User already exists")
        st.stop()

    os.makedirs(user_dir)

    fp_features=[]
    ir_features=[]

    for f in fp_files:
        img=Image.open(f)
        fp_features.append(extract_features(img))

    for f in ir_files:
        img=Image.open(f)
        ir_features.append(extract_features(img))

    np.save(os.path.join(user_dir,"fingerprint.npy"),np.array(fp_features))
    np.save(os.path.join(user_dir,"iris.npy"),np.array(ir_features))

    st.success("User enrolled successfully")
