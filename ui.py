# ui.py

import matplotlib.pyplot as plt

def plot_schedule(start, sequence, algo, direction, wrap_moves=None):
    fig, ax = plt.subplots()
    x_vals = [start] + sequence
    steps = list(range(len(x_vals)))
    ax.plot(steps, x_vals, marker='o', color='blue', label='Head Movement')

    for i, txt in enumerate(x_vals):
        ax.annotate(f"{txt}", (steps[i], x_vals[i]), textcoords="offset points", xytext=(0,5), ha='center')

    if wrap_moves:
        for move in wrap_moves:
            s_idx = x_vals.index(move[0])
            ax.plot([s_idx, s_idx+1], [move[0], move[1]], linestyle='dashed', color='red', label='Wrap-around')

    ax.set_title(f"{algo} ({direction})")
    ax.set_xlabel("Step")
    ax.set_ylabel("Cylinder")
    ax.grid(True)
    ax.legend()
    return fig

def get_requests_from_editor(dataframe):
    try:
        return [int(row["Request"]) for _, row in dataframe.iterrows() if row["Request"] >= 0]
    except:
        return []
