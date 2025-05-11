import streamlit as st
import matplotlib.pyplot as plt
from scan import run_scan
from cscan import run_cscan

def run_ui():
    # Page config
    st.set_page_config(
        page_title="🖩 Disk Scheduling Visualizer",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # === Custom CSS for modern look ===
    st.markdown("""
        <style>
        /* Main container padding */
        .main > div {
            padding: 2rem;
        }
        
        /* Input labels */
        label {
            font-size: 16px !important;
            color: #1f1f1f !important;
            font-weight: 500 !important;
        }
        
        /* Number input styling */
        .stNumberInput input {
            border: 2px solid #2B7DE9;
            border-radius: 8px;
            padding: 12px !important;
        }
        
        /* Plot styling */
        .stPlot {
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Error messages */
        .stAlert {
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # === Title & Description ===
    st.title("💾 Disk Scheduling Algorithms")
    st.markdown("Visualize **SCAN** and **C-SCAN** disk scheduling with accurate head movement tracking.")

    # === Input Section ===
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

        algo_col, dir_col = st.columns(2)
        with algo_col:
            algo = st.selectbox(
                "⚙️ Algorithm",
                ("SCAN", "C-SCAN"),
                help="Choose disk scheduling algorithm"
            )
            
        with dir_col:
            direction = st.radio(
                "🧭 Direction",
                ("right", "left"),
                horizontal=True
            )

        max_cylinder = None
        if algo == "C-SCAN":
            max_cylinder = st.number_input(
                "🔝 Maximum cylinder",
                min_value=1,
                max_value=9999,
                value=200,
                step=1,
                help="Maximum cylinder number for C-SCAN"
            )

        submitted = st.form_submit_button("🚀 Run Simulation")

    # === Input Validation ===
    if submitted:
        error = None
        try:
            requests = list(map(int, raw_requests.strip().split(',')))
            if any(r < 0 for r in requests):
                error = "Negative values in disk requests!"
            if start < 0:
                error = "Initial head position cannot be negative!"
            if max_cylinder and (start > max_cylinder):
                error = "Initial head exceeds maximum cylinder!"
        except ValueError:
            error = "Invalid input format - use comma-separated integers"
        
        if error:
            st.error(f"❌ {error}")
            return

        # === Run Algorithm ===
        with st.spinner("Calculating optimal path..."):
            if algo == "SCAN":
                sequence, movement = run_scan(requests, start, direction)
            else:
                sequence, movement = run_cscan(requests, start, direction, max_cylinder - 1)

        # === Results Display ===
        st.success(f"✅ Total head movement: **{movement}** cylinders")
        
        with st.expander("📜 Detailed Sequence", expanded=True):
            st.markdown(f"``````")

        # === Visualization ===
        fig, ax = plt.subplots(figsize=(10, 5))
        x_vals = [start] + sequence
        ax.plot(range(len(x_vals)), x_vals, 'o-', color='#2B7DE9', linewidth=2, markersize=8)
        
        # Annotate start and end points
        ax.annotate(f'Start ({start})', (0, start), 
                   xytext=(-20,20), textcoords='offset points',
                   arrowprops=dict(arrowstyle="->", color='#1f1f1f'))
        
        if max_cylinder and algo == "C-SCAN":
            ax.axhline(y=max_cylinder-1, color='#ff4b4b', linestyle='--', linewidth=1)
        
        ax.set_title(f"{algo} Algorithm ({direction.title()} Direction)", pad=20)
        ax.set_xlabel("Step Number", labelpad=15)
        ax.set_ylabel("Cylinder Number", labelpad=15)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#f8f9fa')
        
        st.pyplot(fig)

if __name__ == "__main__":
    run_ui()
