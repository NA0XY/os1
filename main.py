# main.py
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time

# Dummy SCAN and C-SCAN algorithms
def run_scan(requests, head, direction):
    sequence = []
    movement = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    if direction == 'left':
        sequence = left[::-1] + right
    else:
        sequence = right + left[::-1]

    current = head
    for r in sequence:
        movement += abs(current - r)
        current = r
    return sequence, movement

def run_cscan(requests, head, direction, max_cylinder):
    sequence = []
    movement = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    if direction == 'left':
        sequence = left[::-1] + right[::-1]
        if right:
            movement += abs(head - 0)
            movement += abs(max_cylinder - 0)
            movement += abs(max_cylinder - right[-1])
        elif left:
            movement += abs(head - left[0])
    else:
        sequence = right + left
        if left:
            movement += abs(head - max_cylinder)
            movement += abs(max_cylinder - 0)
            movement += abs(left[0] - 0)
        elif right:
            movement += abs(head - right[-1])
    return sequence, movement

def plot_sequence(start, sequence, algo, direction, wrap_points=[], current_step=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    x_points = [start] + sequence
    steps = list(range(len(x_points)))
    color = 'blue' if algo == 'SCAN' else 'green'

    ax.plot(steps, x_points, color=color, marker='o', linestyle='None')

    end_idx = current_step + 1 if current_step is not None else len(x_points)
    for i in range(1, end_idx):
        is_wrap = (x_points[i-1], x_points[i]) in wrap_points
        linestyle = '--' if is_wrap else '-'
        ax.plot([i-1, i], [x_points[i-1], x_points[i]], linestyle=linestyle, color=color, marker='o')

    for i, val in enumerate(x_points):
        ax.annotate(str(val), (i, val), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

    ax.set_title(f"{algo} Scheduling ({direction}){' - Step '+str(current_step) if current_step is not None else ''}")
    ax.set_xlabel("Step")
    ax.set_ylabel("Cylinder")
    ax.grid(True)
    plt.tight_layout()
    return fig

def run_ui():
    st.set_page_config(page_title="Disk Scheduling Visualizer", layout="centered")
    st.title("💾 Disk Scheduling Visualizer")

    with st.sidebar:
        default_requests = pd.DataFrame({"Request": [82, 170, 43, 140, 24, 16, 190, 50, 99, 120, 30, 80]})
        request_df = st.data_editor(default_requests, num_rows="dynamic")
        requests = list(map(int, request_df["Request"].dropna()))
        if any(r < 0 for r in requests):
            st.error("Disk requests must be non-negative integers.")
            return

        max_cylinder = st.slider("Max Cylinder", 1, 200, 199)
        start = st.slider("Initial Head Position", 0, max_cylinder, 50)
        algo = st.selectbox("Algorithm", ["SCAN", "C-SCAN"])
        direction = st.radio("Direction", ["right", "left"])
        step_by_step = st.checkbox("Enable Step-by-Step Animation")
        st.slider("Animation Speed (steps/sec)", 1, 5, 2, key='anim_speed')
        run_clicked = st.button("Run")

    # Initialize session state
    for key in ['sequence', 'movement', 'wrap_points', 'anim_running', 'current_step']:
        if key not in st.session_state:
            st.session_state[key] = 0 if key == 'current_step' else []

    if run_clicked:
        st.session_state['current_step'] = 0
        st.session_state['anim_running'] = step_by_step

        if algo == "SCAN":
            seq, mov = run_scan(requests, start, direction)
            wrap_points = []
        else:
            seq, mov = run_cscan(requests, start, direction, max_cylinder)
            wrap_points = []
            if direction == 'right':
                right = sorted([r for r in requests if r >= start])
                left = sorted([r for r in requests if r < start])
                if right: wrap_points.append((right[-1], max_cylinder))
                if left: 
                    wrap_points.append((max_cylinder, 0))
                    wrap_points.append((0, left[0]))
            else:
                left = sorted([r for r in requests if r < start])
                right = sorted([r for r in requests if r >= start])
                if left: wrap_points.append((left[0], 0))
                if right:
                    wrap_points.append((0, max_cylinder))
                    wrap_points.append((max_cylinder, right[-1]))

        st.session_state['sequence'] = seq
        st.session_state['movement'] = mov
        st.session_state['wrap_points'] = wrap_points

    # Plot
    plot_spot = st.empty()
    status = st.empty()

    if st.session_state['sequence']:
        if step_by_step:
            if st.session_state['current_step'] < len(st.session_state['sequence']):
                fig = plot_sequence(start, st.session_state['sequence'], algo, direction, st.session_state['wrap_points'], st.session_state['current_step'])
                plot_spot.pyplot(fig, use_container_width=True)

                if st.session_state['current_step'] == 0:
                    status.markdown(f"**Initial position:** {start}")
                else:
                    cur = st.session_state['sequence'][st.session_state['current_step']]
                    prev = st.session_state['sequence'][st.session_state['current_step'] - 1]
                    step_move = abs(cur - prev)
                    status.markdown(f"**Step {st.session_state['current_step']}** - Moved {step_move} cylinders")

                st.session_state['current_step'] += 1
                time.sleep(1 / st.session_state['anim_speed'])
                st.rerun()
            else:
                status.success(f"Complete! Total head movement: {st.session_state['movement']} cylinders")
                fig = plot_sequence(start, st.session_state['sequence'], algo, direction, st.session_state['wrap_points'])
                plot_spot.pyplot(fig, use_container_width=True)
        else:
            st.success(f"Total head movement: {st.session_state['movement']} cylinders")
            st.code(" → ".join(map(str, st.session_state['sequence'])))
            fig = plot_sequence(start, st.session_state['sequence'], algo, direction, st.session_state['wrap_points'])
            st.pyplot(fig, use_container_width=True)

if __name__ == "__main__":
    run_ui()
