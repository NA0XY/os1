import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time
from scan import run_scan
from cscan import run_cscan

def plot_sequence(start, sequence, algo, direction, wrap_points=[], current_step=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    x_points = [start] + sequence
    steps = list(range(len(x_points)))
    color = 'blue' if algo == 'SCAN' else 'green'

    # Plot points
    ax.plot(steps, x_points, color=color, marker='o', linestyle='None')

    # Draw lines up to current step
    end_idx = current_step + 1 if current_step is not None else len(x_points)
    for i in range(1, end_idx):
        is_wrap = (x_points[i - 1], x_points[i]) in wrap_points
        linestyle = '--' if is_wrap else '-'
        ax.plot([i - 1, i], [x_points[i - 1], x_points[i]], linestyle=linestyle, color=color, marker='o')

    # Annotate points
    for i, val in enumerate(x_points):
        ax.annotate(str(val), (i, val), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

    title = f"{algo} Scheduling ({direction})"
    if current_step is not None:
        title += f" - Step {current_step}"
    ax.set_title(title)
    ax.set_xlabel("Step")
    ax.set_ylabel("Cylinder")
    ax.grid(True)
    plt.tight_layout()
    return fig

def run_ui():
    st.set_page_config(page_title="Disk Scheduling Visualizer", layout="centered")

    st.title("💾 Disk Scheduling Visualizer")
    st.write("Visualize **SCAN** and **C-SCAN** disk scheduling algorithms with step-by-step animation and comparison.")

    default_requests = pd.DataFrame({"Request": [82, 170, 43, 140, 24, 16, 190, 50, 99, 120, 30, 80]})

    try:
        request_df = st.data_editor(data=default_requests, num_rows="dynamic")
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

    max_cylinder_default = 199
    start = st.slider("Initial Head Position", 0, max_cylinder_default, 50)
    algo = st.selectbox("Algorithm", ["SCAN", "C-SCAN"])
    direction = st.radio("Direction", ["right", "left"])

    max_cylinder = max_cylinder_default
    if algo == "C-SCAN":
        max_cylinder = st.number_input("Max Cylinder", min_value=1, value=max_cylinder_default)

    comparison_mode = st.checkbox("Compare SCAN vs C-SCAN")
    step_by_step = st.checkbox("Enable Step-by-Step Animation")

    # Initialize session state variables once
    if 'sequence' not in st.session_state:
        st.session_state.sequence = []
    if 'movement' not in st.session_state:
        st.session_state.movement = 0
    if 'wrap_points' not in st.session_state:
        st.session_state.wrap_points = []
    if 'algo' not in st.session_state:
        st.session_state.algo = algo
    if 'direction' not in st.session_state:
        st.session_state.direction = direction
    if 'start' not in st.session_state:
        st.session_state.start = start
    if 'max_cylinder' not in st.session_state:
        st.session_state.max_cylinder = max_cylinder
    if 'anim_running' not in st.session_state:
        st.session_state.anim_running = False
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'anim_speed' not in st.session_state:
        st.session_state.anim_speed = 1

    # Placeholders for animation plot and status
    status_text = st.empty()
    plot_spot = st.empty()

    if st.button("Run Scheduling"):
        st.session_state.algo = algo
        st.session_state.direction = direction
        st.session_state.start = start
        st.session_state.max_cylinder = max_cylinder
        st.session_state.anim_running = step_by_step
        st.session_state.current_step = 0

        if comparison_mode:
            st.session_state.sequence = None  # Disable single animation
            st.session_state.movement = None
            st.session_state.wrap_points = None
        else:
            if algo == "SCAN":
                seq, mov = run_scan(requests, start, direction)
                wrap_points = []
            else:
                seq, mov = run_cscan(requests, start, direction, max_cylinder)
                requests_sorted = sorted(requests)
                left = [r for r in requests_sorted if r < start]
                right = [r for r in requests_sorted if r >= start]
                if direction == 'right':
                    wrap_points = []
                    if right:
                        wrap_points.append((right[-1], max_cylinder))
                    if left:
                        wrap_points.append((max_cylinder, 0))
                        wrap_points.append((0, left[0]))
                else:
                    wrap_points = []
                    if left:
                        wrap_points.append((left[0], 0))
                    if right:
                        wrap_points.append((0, max_cylinder))
                        wrap_points.append((max_cylinder, right[-1]))
            st.session_state.sequence = seq
            st.session_state.movement = mov
            st.session_state.wrap_points = wrap_points

    # Comparison Mode Display
    if comparison_mode and st.session_state.sequence is None:
        scan_seq, scan_mov = run_scan(requests, start, direction)
        cscan_seq, cscan_mov = run_cscan(requests, start, direction, max_cylinder)

        requests_sorted = sorted(requests)
        left = [r for r in requests_sorted if r < start]
        right = [r for r in requests_sorted if r >= start]
        if direction == 'right':
            wrap_points_cscan = []
            if right:
                wrap_points_cscan.append((right[-1], max_cylinder))
            if left:
                wrap_points_cscan.append((max_cylinder, 0))
                wrap_points_cscan.append((0, left[0]))
        else:
            wrap_points_cscan = []
            if left:
                wrap_points_cscan.append((left[0], 0))
            if right:
                wrap_points_cscan.append((0, max_cylinder))
                wrap_points_cscan.append((max_cylinder, right[-1]))

        empty1, col1, empty2, col2, empty3 = st.columns([0.1, 4.5, 0.1, 4.5, 0.1])

        with col1:
            st.write("### SCAN Algorithm")
            st.success(f"Total head movement: {scan_mov} cylinders")
            st.code(" → ".join(map(str, scan_seq)), language="text")
            fig_scan = plot_sequence(start, scan_seq, "SCAN", direction, wrap_points=[])
            st.pyplot(fig_scan, use_container_width=True)

        with col2:
            st.write("### C-SCAN Algorithm")
            st.success(f"Total head movement: {cscan_mov} cylinders")
            st.code(" → ".join(map(str, cscan_seq)), language="text")
            fig_cscan = plot_sequence(start, cscan_seq, "C-SCAN", direction, wrap_points=wrap_points_cscan)
            st.pyplot(fig_cscan, use_container_width=True)

        st.warning("Step-by-step animation is disabled in comparison mode.")

    # Single Algorithm Mode: Animation or final result
    elif st.session_state.sequence:
        if step_by_step:
            st.subheader("Step-by-Step Animation")

            speed = st.slider("Animation Speed (steps per second)", 1, 5, st.session_state.anim_speed, key='anim_speed')

            col1, col2 = st.columns(2)
            with col1:
                if st.button("⏸ Pause" if st.session_state.anim_running else "▶ Resume"):
                    st.session_state.anim_running = not st.session_state.anim_running
            with col2:
                if st.button("🔄 Reset"):
                    st.session_state.current_step = 0
                    st.session_state.anim_running = False

            if st.session_state.anim_running and st.session_state.current_step < len(st.session_state.sequence):
                fig = plot_sequence(
                    st.session_state.start,
                    st.session_state.sequence,
                    st.session_state.algo,
                    st.session_state.direction,
                    st.session_state.wrap_points,
                    current_step=st.session_state.current_step
                )
                plot_spot.pyplot(fig)

                if st.session_state.current_step == 0:
                    status_text.markdown(f"**Initial position:** {st.session_state.start}")
                else:
                    step_movement = abs(st.session_state.sequence[st.session_state.current_step] - st.session_state.sequence[st.session_state.current_step - 1])
                    status_text.markdown(f"""
                        **Step {st.session_state.current_step}**  
                        - Current Cylinder: {st.session_state.sequence[st.session_state.current_step]}  
                        - Movement: +{step_movement} cylinders
                    """)

                st.session_state.current_step += 1
                time.sleep(1 / speed)
                st.experimental_rerun()

            elif st.session_state.current_step >= len(st.session_state.sequence):
                status_text.success(f"Animation complete! Total movement: {st.session_state.movement} cylinders")
                fig_final = plot_sequence(st.session_state.start, st.session_state.sequence, st.session_state.algo, st.session_state.direction, st.session_state.wrap_points)
                plot_spot.pyplot(fig_final)

        else:
            st.success(f"Total head movement: {st.session_state.movement} cylinders")
            st.code(" → ".join(map(str, st.session_state.sequence)), language="text")
            fig = plot_sequence(st.session_state.start, st.session_state.sequence, st.session_state.algo, st.session_state.direction, st.session_state.wrap_points)
            st.pyplot(fig, use_container_width=True)

if __name__ == "__main__":
    run_ui()
