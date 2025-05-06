import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from scan import run_scan
from cscan import run_cscan

def plot_sequence(start, sequence, algo, direction, wrap_points=[]):
    fig, ax = plt.subplots()
    x_points = [start] + sequence
    steps = list(range(len(x_points)))
    colors = 'blue' if algo == 'SCAN' else 'green'

    for i in range(1, len(x_points)):
        is_wrap = (x_points[i - 1], x_points[i]) in wrap_points
        style = '--' if is_wrap else '-'
        ax.plot([i - 1, i], [x_points[i - 1], x_points[i]],
                linestyle=style, color=colors, marker='o')

    for i, val in enumerate(x_points):
        ax.annotate(f"{val}", (i, val), textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=8)

    ax.set_title(f"{algo} Scheduling ({direction})")
    ax.set_xlabel("Step")
    ax.set_ylabel("Cylinder")
    ax.grid(True)
    st.pyplot(fig)

def run_ui():
    st.set_page_config(page_title="Disk Scheduling Visualizer", layout="centered")

    st.title("💾 Disk Scheduling Visualizer")
    st.write("Visualize **SCAN** and **C-SCAN** algorithms with color-coded movement and annotations.")

    default_requests = pd.DataFrame({"Request": [82, 170, 43, 140, 24, 16, 190]})
    request_df = st.data_editor(
        label="Disk Requests (edit/add rows)", data=default_requests
    )

    try:
        requests = list(map(int, request_df["Request"].dropna()))
    except Exception:
        st.error("Invalid request entries.")
        return

    if not requests:
        st.warning("Please enter at least one request.")
        return

    start = st.slider("Initial Head Position", 0, 199, 50)
    algo = st.selectbox("Algorithm", ["SCAN", "C-SCAN"])
    direction = st.radio("Direction", ["right", "left"])
    max_cylinder = st.number_input("Max Cylinder", min_value=1, value=199) if algo == "C-SCAN" else None

    if st.button("Run Scheduling"):
        if algo == "SCAN":
            sequence, movement = run_scan(requests, start, direction)
            wrap_points = []
        else:
            full_seq = []
            requests_sorted = sorted(requests)
            left = [r for r in requests_sorted if r < start]
            right = [r for r in requests_sorted if r >= start]
            if direction == 'right':
                full_seq = right + [max_cylinder, 0] + left
                wrap_points = [(right[-1], max_cylinder), (max_cylinder, 0), (0, left[0])] if left and right else []
            else:
                full_seq = list(reversed(left)) + [0, max_cylinder] + list(reversed(right))
                wrap_points = [(left[0], 0), (0, max_cylinder), (max_cylinder, right[-1])] if left and right else []
            sequence, movement = run_cscan(requests, start, direction, max_cylinder)

        st.subheader("Results")
        st.success(f"Total head movement: {movement} cylinders")
        st.code(" → ".join(map(str, sequence)), language="text")
        plot_sequence(start, sequence, algo, direction, wrap_points=wrap_points)
