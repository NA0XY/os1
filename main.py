# main.py

import streamlit as st
import pandas as pd
from scan import run_scan
from cscan import run_cscan
from ui import plot_schedule, get_requests_from_editor

st.set_page_config(
    page_title="Disk Scheduling Visualizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💿 Disk Scheduling Visualizer")

st.markdown("Enter disk requests below. Use the sidebar to adjust parameters.")

default_requests = pd.DataFrame({"Request": [82, 170, 43, 140, 24, 16, 190]})
request_df = st.data_editor("Disk Requests (edit/add rows)", default_requests)

requests = get_requests_from_editor(request_df)

st.sidebar.header("Settings")

start = st.sidebar.slider("Initial Head Position", min_value=0, max_value=199, value=50)
direction = st.sidebar.radio("Direction", ("right", "left"))
max_cylinder = st.sidebar.slider("Max Cylinder", min_value=50, max_value=1000, value=199)
mode = st.sidebar.selectbox("Mode", ("Single Algorithm", "Compare SCAN vs C-SCAN"))

if st.sidebar.button("Run Scheduling"):
    if not requests:
        st.error("Please enter at least one valid disk request.")
    else:
        if mode == "Single Algorithm":
            algo = st.sidebar.selectbox("Algorithm", ("SCAN", "C-SCAN"))
            if algo == "SCAN":
                sequence, movement = run_scan(requests, start, direction)
                fig = plot_schedule(start, sequence, algo, direction)
            else:
                sequence, movement, wrap = run_cscan(requests, start, direction, max_cylinder)
                fig = plot_schedule(start, sequence, algo, direction, wrap)

            st.subheader(f"{algo} Results")
            st.success(f"Total head movement: {movement} cylinders")
            st.code(" → ".join(map(str, sequence)))
            st.pyplot(fig)

        elif mode == "Compare SCAN vs C-SCAN":
            col1, col2 = st.columns(2)

            # SCAN
            scan_seq, scan_mv = run_scan(requests, start, direction)
            fig_scan = plot_schedule(start, scan_seq, "SCAN", direction)
            # CSCAN
            cscan_seq, cscan_mv, wrap = run_cscan(requests, start, direction, max_cylinder)
            fig_cscan = plot_schedule(start, cscan_seq, "C-SCAN", direction, wrap)

            with col1:
                st.subheader("SCAN")
                st.success(f"Movement: {scan_mv}")
                st.code(" → ".join(map(str, scan_seq)))
                st.pyplot(fig_scan)

            with col2:
                st.subheader("C-SCAN")
                st.success(f"Movement: {cscan_mv}")
                st.code(" → ".join(map(str, cscan_seq)))
                st.pyplot(fig_cscan)
