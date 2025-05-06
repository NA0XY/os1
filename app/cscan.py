def run_cscan(requests, start, direction, max_cylinder):
    requests.sort()
    sequence = []
    movement = 0
    if direction == "right":
        sequence = [start] + [r for r in requests if r >= start] + [max_cylinder] + [r for r in requests if r < start]
    else:
        sequence = [start] + [r for r in requests if r <= start] + [0] + [r for r in requests if r > start]
    for i in range(1, len(sequence)):
        movement += abs(sequence[i] - sequence[i-1])
    return sequence, movement
