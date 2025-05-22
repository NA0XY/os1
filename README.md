# Disk Scheduling Visualizer

This project is an interactive web application for visualizing and comparing classic disk scheduling algorithms: **SCAN, C-SCAN, LOOK, and C-LOOK**. It is designed as an educational tool to help students and enthusiasts understand the behavior and efficiency of these algorithms in operating systems.

## Features

- **Simulate and visualize** the execution of SCAN, C-SCAN, LOOK, and C-LOOK algorithms.
- **Interactive web UI** built with Streamlit for easy user input and instant results.
- **Side-by-side comparison** of all algorithms on the same set of disk requests.
- **Efficiency metrics**: displays total head movements and highlights the most/least efficient algorithm for your input.
- **Clear explanations** and characteristics for each algorithm.
- **Error handling** for invalid or out-of-range disk requests.


## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip

### Installation

1. **Clone this repository:**
   ```sh
   git clone https://github.com/NA0XY/os1.git
   cd os1
   ```

2. **Install dependencies:**
   ```sh
   pip install streamlit plotly
   ```

### Running the Application

Start the Streamlit app with:
```sh
streamlit run main.py
```
This will open the application in your default web browser.

## Usage

1. Enter a comma-separated list of disk requests (e.g., `82,170,43,140,24,16,190`).
2. Set the initial head position and the maximum cylinder value.
3. Select the direction (left or right).
4. Choose an algorithm or "Compare All" to see all at once.
5. Click "Run Simulation" to see the sequence, total head movement, and visualizations.

## Algorithms Explained

- **SCAN (Elevator Algorithm):** Services requests in one direction until the end, then reverses direction.
- **C-SCAN (Circular SCAN):** Services requests in one direction, jumps back to the start after reaching the end.
- **LOOK:** Like SCAN, but only goes as far as the last request in each direction.
- **C-LOOK:** Like C-SCAN, but only goes as far as the last request before jumping.

## Project Structure

```
os1/
│
├── main.py         # Entry point for running the Streamlit UI
├── ui.py           # UI logic and algorithm orchestration
├── scan.py         # SCAN algorithm implementation
├── cscan.py        # C-SCAN algorithm implementation
├── look.py         # LOOK algorithm implementation
├── clook.py        # C-LOOK algorithm implementation
└── README.md       # Project documentation
```

## Innovation

- **Interactive Visualization:** Makes algorithm behavior clear and engaging.
- **Educational Focus:** Explains each algorithm’s properties and highlights efficiency.
- **Comparison Tools:** Unique side-by-side metrics and plots for direct comparison.

## Contributing

Contributions, suggestions, and bug reports are welcome! Please open an issue or submit a pull request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- Inspired by standard Operating Systems textbooks and educational resources.
- Built using [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/python/).
