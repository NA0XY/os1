
import streamlit as st
from scan import run_scan
from cscan import run_cscan
import matplotlib.pyplot as plt

def main():
    st.title("Disk Scheduling Visualizer")
    st.write("This app demonstrates SCAN and C-SCAN disk scheduling algorithms.")

    requests = st.text_input("Enter disk requests (comma-separated):", "82, 170, 43, 140, 24, 16, 190")
    request_list = list(map(int, requests.split(',')))
    head = st.slider("Initial Head Position", 0, 199, 50)
    algo = st.selectbox("Algorithm", ["SCAN", "C-SCAN"])
    direction = st.radio("Direction", ["left", "right"])

    if st.button("Run Scheduling"):
        if algo == "SCAN":
            sequence, movement = run_scan(request_list, head, direction)
        else:
            sequence, movement, _ = run_cscan(request_list, head, direction, 199)

        st.success(f"Total head movement: {movement} cylinders")
        st.code(" → ".join(map(str, sequence)))

if __name__ == "__main__":
    main()
