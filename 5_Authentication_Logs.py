import streamlit as st
import pandas as pd
import os
import csv

st.title("📊 Authentication Logs")

log_file = "auth_log.csv"


# -------- CREATE FILE IF MISSING --------
if not os.path.exists(log_file):

    with open(log_file,"w",newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Timestamp",
            "User",
            "Fingerprint Score",
            "Iris Score",
            "Fusion Score",
            "Result"
        ])


# -------- READ LOGS --------
df = pd.read_csv(log_file)


# -------- METRICS --------
total_attempts = len(df)
success = len(df[df["Result"] == "GRANTED"])
failed = len(df[df["Result"] == "DENIED"])


col1,col2,col3 = st.columns(3)

col1.metric("Total Attempts", total_attempts)
col2.metric("Successful Logins", success)
col3.metric("Failed Attempts", failed)

st.divider()


st.dataframe(df, use_container_width=True)
