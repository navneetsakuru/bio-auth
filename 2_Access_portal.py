import streamlit as st
import numpy as np
import os
import csv
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

from training.feature_extractor import extract_features


# ---------------- CONFIG ----------------
TEMPLATE_DIR = "templates"
THRESHOLD = 0.80
LOG_FILE = "auth_log.csv"

EMAIL_SENDER = "navneetsakuru@gmail.com"
EMAIL_PASSWORD = "uqefzaqpkojdnsyw"
EMAIL_RECEIVER = "navneetsakuru@gmail.com"


# ---------------- SESSION STATE ----------------
if "fail_count" not in st.session_state:
    st.session_state.fail_count = 0

if "lock_until" not in st.session_state:
    st.session_state.lock_until = 0


# ---------------- EMAIL ALERT ----------------
def send_security_email():

    subject = "Biometric Security Alert"

    body = """
Multiple failed biometric authentication attempts detected.

The biometric system has been locked for 30 seconds.

Possible unauthorized access attempt.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        server.sendmail(
            EMAIL_SENDER,
            EMAIL_RECEIVER,
            msg.as_string()
        )

        server.quit()

    except:
        pass


# ---------------- LOG FUNCTION ----------------
def log_attempt(user, fp_score, ir_score, fusion_score, result):

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "Timestamp",
                "User",
                "Fingerprint Score",
                "Iris Score",
                "Fusion Score",
                "Result"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user,
            round(fp_score,3),
            round(ir_score,3),
            round(fusion_score,3),
            result
        ])


# ---------------- PAGE ----------------
st.title("🔐 Access Portal")


# ---------------- LOCK CHECK ----------------
if time.time() < st.session_state.lock_until:

    remaining = int(st.session_state.lock_until - time.time())

    st.error(f"System locked. Try again in {remaining} seconds.")

    st.stop()


# ---------------- FILE UPLOAD ----------------
col1, col2 = st.columns(2)

with col1:
    fp_file = st.file_uploader(
        "Upload Fingerprint",
        type=["jpg","jpeg","png","bmp"]
    )

with col2:
    ir_file = st.file_uploader(
        "Upload Iris",
        type=["jpg","jpeg","png","bmp"]
    )


# ---------------- AUTHENTICATION ----------------
if st.button("Authenticate"):

    if fp_file is None or ir_file is None:
        st.warning("Upload both fingerprint and iris")
        st.stop()


    fp_img = Image.open(fp_file)
    ir_img = Image.open(ir_file)


    fp_feat = extract_features(fp_img)
    ir_feat = extract_features(ir_img)


    best_fp_person = None
    best_ir_person = None

    best_fp_score = 0
    best_ir_score = 0


    # ---------------- MATCHING ----------------
    for person in os.listdir(TEMPLATE_DIR):

        person_dir = os.path.join(TEMPLATE_DIR, person)

        if not os.path.isdir(person_dir):
            continue


        fp_templates = np.load(os.path.join(person_dir,"fingerprint.npy"))
        ir_templates = np.load(os.path.join(person_dir,"iris.npy"))


        fp_score = max(
            cosine_similarity(fp_feat.reshape(1,-1),t.reshape(1,-1))[0][0]
            for t in fp_templates
        )


        ir_score = max(
            cosine_similarity(ir_feat.reshape(1,-1),t.reshape(1,-1))[0][0]
            for t in ir_templates
        )


        if fp_score > best_fp_score:
            best_fp_score = fp_score
            best_fp_person = person

        if ir_score > best_ir_score:
            best_ir_score = ir_score
            best_ir_person = person


    # ---------------- DECISION ----------------
    if best_fp_person == best_ir_person:

        fusion = (best_fp_score + best_ir_score)/2


        if fusion >= THRESHOLD:

            st.success(f"ACCESS GRANTED → {best_fp_person}")

            log_attempt(
                best_fp_person,
                best_fp_score,
                best_ir_score,
                fusion,
                "GRANTED"
            )

            st.session_state.fail_count = 0

            st.session_state["authenticated"] = True
            st.session_state["user"] = best_fp_person

            time.sleep(1)

            # 🔹 Redirect to Dashboard
            st.switch_page("pages/1_Dashboard.py")


        else:

            st.error("ACCESS DENIED")

            log_attempt(
                "Unknown",
                best_fp_score,
                best_ir_score,
                fusion,
                "DENIED"
            )

            st.session_state.fail_count += 1


    else:

        st.error("ACCESS DENIED — biometrics mismatch")

        log_attempt(
            "Mismatch",
            best_fp_score,
            best_ir_score,
            0,
            "DENIED"
        )

        st.session_state.fail_count += 1


    # ---------------- LOCK SYSTEM ----------------
    if st.session_state.fail_count >= 3:

        st.session_state.lock_until = time.time() + 30

        send_security_email()

        st.error("Too many failed attempts. System locked for 30 seconds.")
