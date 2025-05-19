import streamlit as st
import matplotlib.pyplot as plt
from scan import run_scan
from cscan import run_cscan
from look import run_look
from clook import run_clook

def plot_algorithm(ax, sequence, start, title, color):
    x_vals = [start] + sequence
    ax.plot(range(len(x_vals)), x_vals, 'o-', color=color, linewidth=2)
    ax.set_title(title, fontsize=14, pad=10)
    ax.set_xlabel("Step Number", labelpad=10)
    ax.set_ylabel("Cylinder Number", labelpad=10)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')

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
                scan_seq, scan_move = run_scan(requests, start, direction)
                cscan_seq, cscan_move = run_cscan(requests, start, direction, max_cylinder - 1)
                look_seq, look_move = run_look(requests, start, direction)
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

            # Visualization
            fig, axs = plt.subplots(2, 2, figsize=(14, 10))
            plt.subplots_adjust(hspace=0.4, wspace=0.3)  # Add space between the subplots
            plot_algorithm(axs[0, 0], scan_seq, start, f"SCAN ({direction.title()})", '#2B7DE9')
            plot_algorithm(axs[0, 1], cscan_seq, start, f"C-SCAN ({direction.title()})", '#FF4B4B')
            plot_algorithm(axs[1, 0], look_seq, start, f"LOOK ({direction.title()})", '#2ECC71')
            plot_algorithm(axs[1, 1], clook_seq, start, f"C-LOOK ({direction.title()})", '#E67E22')
            st.pyplot(fig)


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
                    sequence, movement = run_scan(requests, start, direction)
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

                fig, ax = plt.subplots(figsize=(10, 5))
                plot_algorithm(ax, sequence, start, f"{algo_name} ({direction.title()})", color)
                st.pyplot(fig)

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
