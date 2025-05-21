import streamlit as st
import plotly.subplots as sp
import plotly.graph_objs as go
from scan import run_scan
from cscan import run_cscan
from look import run_look
from clook import run_clook

ALGO_DESCRIPTIONS = {
    "SCAN": "SCAN (Elevator): Services requests in one direction, then reverses at the end.",
    "C-SCAN": "C-SCAN: Services requests in one direction, jumps to start after reaching end.",
    "LOOK": "LOOK: Like SCAN, but only goes as far as the last request in each direction.",
    "C-LOOK": "C-LOOK: Like C-SCAN, but only goes as far as the last request before jumping."
}

def get_step_explanations(sequence, start, algo_name):
    explanations = []
    algo_desc = ALGO_DESCRIPTIONS[algo_name]
    current = start
    for idx, target in enumerate(sequence):
        if idx == 0:
            step_expl = f"Start at {current}, move to {target} (servicing request)"
        else:
            step_expl = f"Move from {current} to {target} (servicing request)"
        explanations.append(f"{algo_desc}<br>{step_expl}")
        current = target
    # Add explanation for the initial point
    return explanations

def plot_all_algorithms_with_tooltips(start, scan_seq, cscan_seq, look_seq, clook_seq):
    # Each sequence is a list of cylinder numbers (not including the start)
    fig = sp.make_subplots(
        rows=3, cols=2,
        subplot_titles=("SCAN", "C-SCAN", "LOOK", "C-LOOK"),
        vertical_spacing=0.2, horizontal_spacing=0.13
    )

    algos = [
        ("SCAN", scan_seq, '#2B7DE9', 1, 1),
        ("C-SCAN", cscan_seq, '#FF4B4B', 1, 2),
        ("LOOK", look_seq, '#2ECC71', 2, 1),
        ("C-LOOK", clook_seq, '#E67E22', 2, 2)
    ]

    for algo_name, seq, color, row, col in algos:
        x_vals = list(range(len(seq) + 1))
        y_vals = [start] + seq
        explanations = get_step_explanations(seq, start, algo_name)
        explanations = [f"Start at {start}"] + explanations  # Add explanation for initial point

        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines+markers',
                marker=dict(size=10, color=color),
                line=dict(width=3, color=color),
                text=explanations,
                hoverinfo='text+y'
            ),
            row=row, col=col
        )

    fig.update_layout(
        height=1200, width=1800,
        showlegend=False,
        plot_bgcolor="#f8f9fa",
        margin=dict(l=40, r=40, t=100, b=40)
    )
    for i in range(1, 5):
        fig['layout'][f'yaxis{i}']['title'] = 'Cylinder Number'
        fig['layout'][f'xaxis{i}']['title'] = 'Step Number'

    return fig

def run_ui():
    st.set_page_config(
        page_title="🖩 Disk Scheduling Visualizer",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.title("Disk Scheduling Visualizer")
    st.markdown("Compare head movement patterns between **SCAN, C-SCAN, LOOK, and C-LOOK** algorithms.")

    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            raw_requests = st.text_input(
                "Disk requests (comma-separated)",
                value="82,170,43,140,24,16,190",
                help="Enter positive integers between 0-9999"
            )
        with col2:
            start = st.number_input(
                "Initial head position",
                min_value=0,
                max_value=9999,
                value=50,
                step=1
            )

        direction = st.radio(
            "Direction",
            ("right", "left"),
            horizontal=True
        )

        max_cylinder = st.number_input(
            "Maximum cylinder",
            min_value=1,
            max_value=9999,
            value=200,
            step=1,
            help="Required for C-SCAN and C-LOOK algorithms"
        )

        algorithm_choice = st.radio(
            "Algorithm Selection",
            ("SCAN", "C-SCAN", "LOOK", "C-LOOK", "Compare All"),
            horizontal=True
        )

        submitted = st.form_submit_button("Run Simulation")

    if submitted:
        try:
            requests = list(map(int, raw_requests.strip().split(',')))
            if any(r < 0 for r in requests):
                st.error("❌ Negative values in disk requests!")
                return
        except ValueError:
            st.error("❌ Invalid input format!")
            return

        if algorithm_choice == "Compare All":
            with st.spinner("Calculating all algorithms..."):
                scan_seq, scan_move = run_scan(requests, start, direction,max_cylinder)
                cscan_seq, cscan_move = run_cscan(requests, start, direction, max_cylinder - 1)
                look_seq, look_move = run_look(requests, start, direction-1)
                clook_seq, clook_move = run_clook(requests, start, direction, max_cylinder - 1)

            st.subheader("Comparison Results")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("SCAN Total Movement", scan_move)
                st.code(f"Sequence:\n{scan_seq}")
                st.metric("LOOK Total Movement", look_move)
                st.code(f"Sequence:\n{look_seq}")
            with col2:
                st.metric("C-SCAN Total Movement", cscan_move)
                st.code(f"Sequence:\n{cscan_seq}")
                st.metric("C-LOOK Total Movement", clook_move)
                st.code(f"Sequence:\n{clook_seq}")

            # Efficiency comparison
            st.markdown("---")
            algo_movements = {
                "SCAN": scan_move,
                "C-SCAN": cscan_move,
                "LOOK": look_move,
                "C-LOOK": clook_move
            }
            min_movement = min(algo_movements.values())
            efficient_algos = [name for name, mov in algo_movements.items() if mov == min_movement]
            if len(efficient_algos) == 1:
                st.success(f" **Most Efficient:** {efficient_algos[0]} with {min_movement} cylinders")
            else:
                st.success(f" **Tie Between:** {', '.join(efficient_algos)} with {min_movement} cylinders")

            # Plotly interactive visualization with tooltips
            fig = plot_all_algorithms_with_tooltips(
                start, scan_seq, cscan_seq, look_seq, clook_seq
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Key Differences")
            st.table({
                "Feature": ["Direction Handling", "Return Path", "Uniform Wait Time", "Empty End Handling", "Optimal For"],
                "SCAN": ["Reverses direction", "Services return path", "No", "Visits end always", "Moderate loads"],
                "C-SCAN": ["Circular movement", "Jumps to start", "Yes", "Visits end always", "Heavy loads"],
                "LOOK": ["Reverses direction", "Services return path", "No", "Visits only requested cylinders", "Moderate loads"],
                "C-LOOK": ["Circular movement", "Jumps to start", "Yes", "Visits only requested cylinders", "Heavy loads"]
            })

        else:
            with st.spinner("Calculating..."):
                if algorithm_choice == "SCAN":
                    sequence, movement = run_scan(requests, start, direction, max_cylinder)
                    algo_name = "SCAN"
                    color = '#2B7DE9'
                elif algorithm_choice == "C-SCAN":
                    sequence, movement = run_cscan(requests, start, direction, max_cylinder - 1)
                    algo_name = "C-SCAN"
                    color = '#FF4B4B'
                elif algorithm_choice == "LOOK":
                    sequence, movement = run_look(requests, start, direction)
                    algo_name = "LOOK"
                    color = '#2ECC71'
                else:
                    sequence, movement = run_clook(requests, start, direction, max_cylinder - 1)
                    algo_name = "C-LOOK"
                    color = '#E67E22'

                st.subheader("Results")
                st.success(f" Total head movement: **{movement}** cylinders")
                with st.expander("Detailed Sequence", expanded=True):
                    st.code(" → ".join(map(str, sequence)))

                # Plotly single algorithm with tooltips
                x_vals = list(range(len(sequence) + 1))
                y_vals = [start] + sequence
                explanations = get_step_explanations(sequence, start, algo_name)
                explanations = [f"Start at {start}"] + explanations

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode='lines+markers',
                    marker=dict(size=10, color=color),
                    line=dict(width=3, color=color),
                    text=explanations,
                    hoverinfo='text+y'
                ))
                fig.update_layout(
                    title=f"{algo_name} ({direction.title()}) Head Movement",
                    xaxis_title="Step Number",
                    yaxis_title="Cylinder Number",
                    plot_bgcolor="#f8f9fa",
                    height=500, width=900
                )
                st.plotly_chart(fig, use_container_width=True)

                # Algorithm explanations
                if algo_name == "SCAN":
                    st.markdown("**SCAN Algorithm Characteristics:**")
                    st.markdown("- Also known as the elevator algorithm")
                    st.markdown("- Services requests in one direction until end, then reverses")
                elif algo_name == "C-SCAN":
                    st.markdown("**C-SCAN Algorithm Characteristics:**")
                    st.markdown("- Circular version of SCAN")
                    st.markdown("- Treats cylinders as a circular list")
                    st.markdown("- Jumps back to start after reaching end")
                elif algo_name == "LOOK":
                    st.markdown("**LOOK Algorithm Characteristics:**")
                    st.markdown("- Similar to SCAN but only goes as far as the last request in each direction")
                    st.markdown("- Does not go to the end of the disk unless requested")
                else:
                    st.markdown("**C-LOOK Algorithm Characteristics:**")
                    st.markdown("- Circular version of LOOK")
                    st.markdown("- Jumps back to the first request after reaching the last")

if __name__ == "__main__":
    run_ui()
