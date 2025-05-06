def run_scan(requests, start, direction):
    requests.sort()
    sequence = []
    movement = 0
    if direction == "right":
        sequence = [start] + [r for r in requests if r >= start] + [r for r in requests if r < start]
    else:
        sequence = [start] + [r for r in requests if r <= start] + [r for r in requests if r > start]
    for i in range(1, len(sequence)):
        movement += abs(sequence[i] - sequence[i-1])
    return sequence, movement
