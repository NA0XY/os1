import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time
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
    return fig

def run_ui():
    st.set_page_config(page_title="Disk Scheduling Visualizer", layout="centered")

    st.title("💾 Disk Scheduling Visualizer")
    st.write("Visualize **SCAN** and **C-SCAN** algorithms with color-coded movement and annotations.")

    # Initialize a larger default set of requests
    default_requests = pd.DataFrame({"Request": [82, 170, 43, 140, 24, 16, 190, 50, 99, 120, 30, 80]})

    # Using st.data_editor to edit/add rows for disk requests
    try:
        request_df = st.data_editor(data=default_requests, num_rows="dynamic")
        # Validate that disk requests are non-negative integers
        requests = list(map(int, request_df["Request"].dropna()))
        if any(r < 0 for r in requests):
            st.error("Disk requests must be non-negative integers.")
            return
    except Exception as e:
        st.error(f"Error in data_editor: {e}")
        return

    if not requests:
        st.warning("Please enter at least one request.")
        return

    # Ensure initial head position is non-negative and within the range of cylinders
    max_cylinder = 199
    start = st.slider("Initial Head Position", 0, max_cylinder, 50)
    if start < 0:
        st.error("Initial head position must be non-negative.")
        return

    algo = st.selectbox("Algorithm", ["SCAN", "C-SCAN"])
    direction = st.radio("Direction", ["right", "left"])
    if algo == "C-SCAN":
        max_cylinder = st.number_input("Max Cylinder", min_value=1, value=max_cylinder)
        if max_cylinder <= 0:
            st.error("Max cylinder number must be positive.")
            return

    comparison_mode = st.checkbox("Compare SCAN vs C-SCAN")
    step_by_step = st.checkbox("Enable Step-by-Step Animation")

    # Button for running SCAN algorithm individually
    if st.button("Run SCAN Algorithm"):
        sequence, movement = run_scan(requests, start, direction)
        wrap_points = []

        st.subheader("SCAN Algorithm Results")
        st.success(f"Total head movement: {movement} cylinders")
        st.code(" → ".join(map(str, sequence)), language="text")
        fig = plot_sequence(start, sequence, "SCAN", direction, wrap_points=wrap_points)
        st.pyplot(fig)

        if step_by_step:
            animate_sequence(sequence, "SCAN", start, direction, wrap_points=wrap_points)

    # Button for running C-SCAN algorithm individually
    if st.button("Run C-SCAN Algorithm"):
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

        st.subheader("C-SCAN Algorithm Results")
        st.success(f"Total head movement: {movement} cylinders")
        st.code(" → ".join(map(str, sequence)), language="text")
        fig = plot_sequence(start, sequence, "C-SCAN", direction, wrap_points=wrap_points)
        st.pyplot(fig)

        if step_by_step:
            animate_sequence(sequence, "C-SCAN", start, direction, wrap_points=wrap_points)

    # Comparison Mode if selected
    if comparison_mode:
        st.subheader("Comparison Mode Results")
        st.write(f"**SCAN Algorithm**:")
        sequence, movement = run_scan(requests, start, direction)
        st.success(f"Total head movement: {movement} cylinders")
        st.code(" → ".join(map(str, sequence)), language="text")
        fig = plot_sequence(start, sequence, "SCAN", direction, wrap_points=wrap_points)
        st.pyplot(fig)

        st.write(f"**C-SCAN Algorithm**:")
        # Run C-SCAN again for comparison
        cscan_sequence, cscan_movement = run_cscan(requests, start, direction, max_cylinder)
        st.success(f"Total head movement: {cscan_movement} cylinders")
        st.code(" → ".join(map(str, cscan_sequence)), language="text")
        fig = plot_sequence(start, cscan_sequence, "C-SCAN", direction, wrap_points=wrap_points)
        st.pyplot(fig)

    # Step-by-Step Animation
    if step_by_step:
        st.subheader("Step-by-Step Animation")
        placeholder = st.empty()  # Create a placeholder for the animation plot

        def animate_sequence(sequence, algo, start, direction, wrap_points=[]):
            for i in range(len(sequence)):
                # Update the plot with each step
                step_sequence = sequence[:i + 1]
                step_fig = plot_sequence(start, step_sequence, algo, direction, wrap_points=wrap_points)
                placeholder.pyplot(step_fig)  # Display the updated plot in the placeholder
                st.write(f"Step {i + 1}: Move to cylinder {sequence[i]}")
                time.sleep(1)

        # Choose algorithm to animate
        if algo == "SCAN":
            animate_sequence(sequence, "SCAN", start, direction, wrap_points=wrap_points)
        else:
            animate_sequence(sequence, "C-SCAN", start, direction, wrap_points=wrap_points)
