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

    # Plot all points
    ax.plot(steps, x_points, color=color, marker='o', linestyle='None')

    # Draw lines up to current step
    end_idx = current_step + 1 if current_step is not None else len(x_points)
    for i in range(1, end_idx):
        is_wrap = (x_points[i-1], x_points[i]) in wrap_points
        linestyle = '--' if is_wrap else '-'
        ax.plot([i-1, i], [x_points[i-1], x_points[i]], 
                linestyle=linestyle, color=color, marker='o')

    # Annotate points
    for i, val in enumerate(x_points):
        ax.annotate(str(val), (i, val), textcoords="offset points", 
                   xytext=(0,10), ha='center', fontsize=8)

    ax.set_title(f"{algo} Scheduling ({direction}){' - Step '+str(current_step) if current_step else ''}")
    ax.set_xlabel("Step")
    ax.set_ylabel("Cylinder")
    ax.grid(True)
    plt.tight_layout()
    return fig

def run_ui():
    st.set_page_config(page_title="Disk Scheduling Visualizer", layout="centered")
    
    # Persistent UI elements
    st.title("💾 Disk Scheduling Visualizer")
    st.write("Visualize **SCAN** and **C-SCAN** algorithms with step-by-step animation")

    # Session state initialization
    if 'run_setup' not in st.session_state:
        st.session_state.update({
            'sequence': [],
            'movement': 0,
            'wrap_points': [],
            'anim_running': False,
            'current_step': 0,
            'anim_speed': 1,
            'plot_spot': st.empty(),
            'status_text': st.empty(),
            'run_setup': True
        })

    # Control panel
    with st.sidebar:
        default_requests = pd.DataFrame({"Request": [82, 170, 43, 140, 24, 16, 190, 50, 99, 120, 30, 80]})
        request_df = st.data_editor(default_requests, num_rows="dynamic")
        requests = list(map(int, request_df["Request"].dropna()))
        
        max_cylinder = st.slider("Max Cylinder", 1, 200, 199)
        start = st.slider("Initial Head Position", 0, max_cylinder, 50)
        algo = st.selectbox("Algorithm", ["SCAN", "C-SCAN"])
        direction = st.radio("Direction", ["right", "left"])
        step_by_step = st.checkbox("Enable Animation")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Run Scheduling"):
                if algo == "SCAN":
                    seq, mov = run_scan(requests, start, direction)
                    wrap_points = []
                else:
                    seq, mov = run_cscan(requests, start, direction, max_cylinder)
                    requests_sorted = sorted(requests)
                    left = [r for r in requests_sorted if r < start]
                    right = [r for r in requests_sorted if r >= start]
                    wrap_points = []
                    if direction == 'right':
                        if right: wrap_points.append((right[-1], max_cylinder))
                        if left: 
                            wrap_points.append((max_cylinder, 0))
                            wrap_points.append((0, left[0]))
                    else:
                        if left: wrap_points.append((left[0], 0))
                        if right: 
                            wrap_points.append((0, max_cylinder))
                            wrap_points.append((max_cylinder, right[-1]))
                
                st.session_state.update({
                    'sequence': seq,
                    'movement': mov,
                    'wrap_points': wrap_points,
                    'current_step': 0,
                    'anim_running': step_by_step,
                    'start': start,
                    'algo': algo,
                    'direction': direction
                })
        
        with col2:
            st.session_state.anim_speed = st.slider("Speed", 1, 5, 2)
            if st.button("⏸ Pause" if st.session_state.anim_running else "▶ Resume"):
                st.session_state.anim_running = not st.session_state.anim_running
            if st.button("🔄 Reset"):
                st.session_state.current_step = 0
                st.session_state.anim_running = False

    # Animation core
    if st.session_state.anim_running and st.session_state.current_step < len(st.session_state.sequence):
        # Update plot
        fig = plot_sequence(
            st.session_state.start,
            st.session_state.sequence,
            st.session_state.algo,
            st.session_state.direction,
            st.session_state.wrap_points,
            current_step=st.session_state.current_step
        )
        st.session_state.plot_spot.pyplot(fig)
        
        # Update status
        if st.session_state.current_step == 0:
            st.session_state.status_text.markdown(f"**Initial position:** {st.session_state.start}")
        else:
            step_mov = abs(st.session_state.sequence[st.session_state.current_step] - 
                          st.session_state.sequence[st.session_state.current_step-1])
            st.session_state.status_text.markdown(f"""
                **Step {st.session_state.current_step}**  
                - Current Cylinder: {st.session_state.sequence[st.session_state.current_step]}  
                - Movement: +{step_mov} cylinders
            """)
        
        # Progress animation
        st.session_state.current_step += 1
        time.sleep(1/st.session_state.anim_speed)
        st.rerun()
    
    elif st.session_state.sequence:
        # Final state
        if st.session_state.current_step >= len(st.session_state.sequence):
            st.session_state.status_text.success(f"Complete! Total movement: {st.session_state.movement} cylinders")
            fig = plot_sequence(st.session_state.start, st.session_state.sequence,
                              st.session_state.algo, st.session_state.direction,
                              st.session_state.wrap_points)
            st.session_state.plot_spot.pyplot(fig)
        else:
            # Static result display
            st.session_state.status_text.success(f"Total movement: {st.session_state.movement} cylinders")
            st.session_state.plot_spot.pyplot(
                plot_sequence(st.session_state.start, st.session_state.sequence,
                            st.session_state.algo, st.session_state.direction,
                            st.session_state.wrap_points)
            )

if __name__ == "__main__":
    run_ui()
