
def run_scan(requests, head, direction):
    requests.sort()
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    sequence = []
    if direction == "left":
        sequence = left[::-1] + right
    else:
        sequence = right + left[::-1]

    total_movement = abs(head - sequence[0]) + sum(
        abs(sequence[i] - sequence[i - 1]) for i in range(1, len(sequence))
    )
    return sequence, total_movement
