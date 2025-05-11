import streamlit as st
import matplotlib.pyplot as plt
from scan import run_scan
from cscan import run_cscan

def plot_algorithm(ax, sequence, start, title, color):
    """Helper function to plot algorithm results"""
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

    st.title("💽 SCAN vs C-SCAN Disk Scheduling")
    st.markdown("Compare head movement patterns between SCAN and C-SCAN algorithms")

    with st.form("input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            raw_requests = st.text_input(
                "📋 Disk requests (comma-separated)",
                value="82,170,43,140,24,16,190",
                help="Enter positive integers between 0-9999"
            )
            
        with col2:
            start = st.number_input(
                "🎯 Initial head position",
                min_value=0,
                max_value=9999,
                value=50,
                step=1
            )

        direction = st.radio(
            "🧭 Direction",
            ("right", "left"),
            horizontal=True
        )
        
        max_cylinder = st.number_input(
            "🔝 Maximum cylinder",
            min_value=1,
            max_value=9999,
            value=200,
            step=1,
            help="Required for C-SCAN algorithm"
        )

        compare_mode = st.checkbox("🔀 Compare SCAN vs C-SCAN")

        submitted = st.form_submit_button("🚀 Run Simulation")

    if submitted:
        try:
            requests = list(map(int, raw_requests.strip().split(',')))
            if any(r < 0 for r in requests):
                st.error("❌ Negative values in disk requests!")
                return
        except ValueError:
            st.error("❌ Invalid input format!")
            return

        if compare_mode:
            # Run both algorithms for comparison
            with st.spinner("Calculating both algorithms..."):
                scan_seq, scan_move = run_scan(requests, start, direction)
                cscan_seq, cscan_move = run_cscan(requests, start, direction, max_cylinder - 1)

            # Comparison results
            st.subheader("Comparison Results")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("SCAN Total Movement", scan_move)
                st.code(f"Sequence:\n{scan_seq}")
                
            with col2:
                st.metric("C-SCAN Total Movement", cscan_move)
                st.code(f"Sequence:\n{cscan_seq}")

            # Comparison plot
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            
            plot_algorithm(ax1, scan_seq, start, 
                         f"SCAN ({direction.title()})", '#2B7DE9')
            plot_algorithm(ax2, cscan_seq, start, 
                         f"C-SCAN ({direction.title()})", '#FF4B4B')
            
            st.pyplot(fig)

            # Algorithm comparison table
            st.markdown("### Key Differences")
            st.table({
                "Feature": ["Direction Handling", "Return Path", "Uniform Wait Time", 
                           "Empty End Handling", "Optimal For"],
                "SCAN": ["Reverses direction", "Services return path", "No", 
                        "Visits end always", "Moderate loads"],
                "C-SCAN": ["Circular movement", "Jumps to start", "Yes", 
                          "Visits end always", "Heavy loads"]
            })

        else:
            # Single algorithm mode
            with st.spinner("Calculating..."):
                if compare_mode:
                    algorithm = "SCAN"
                else:
                    algorithm = "SCAN"
                
                if algorithm == "SCAN":
                    sequence, movement = run_scan(requests, start, direction)
                else:
                    sequence, movement = run_cscan(requests, start, direction, max_cylinder - 1)

                st.subheader("Results")
                st.success(f"✅ Total head movement: **{movement}** cylinders")
                
                with st.expander("📜 Detailed Sequence", expanded=True):
                    st.code(" → ".join(map(str, sequence)))

                fig, ax = plt.subplots(figsize=(10, 5))
                plot_algorithm(ax, sequence, start, 
                             f"{algorithm} ({direction.title()})", '#2B7DE9')
                st.pyplot(fig)

if __name__ == "__main__":
    run_ui()
