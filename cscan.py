
def run_cscan(requests, head, direction, max_cylinder):
    requests.sort()
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    sequence = []
    wrap_points = []

    if direction == "right":
        sequence = right + [max_cylinder, 0] + left
        wrap_points = [(right[-1], max_cylinder), (max_cylinder, 0), (0, left[0])] if left else []
    else:
        sequence = left[::-1] + [0, max_cylinder] + right[::-1]
        wrap_points = [(left[0], 0), (0, max_cylinder), (max_cylinder, right[-1])] if right else []

    total_movement = abs(head - sequence[0]) + sum(
        abs(sequence[i] - sequence[i - 1]) for i in range(1, len(sequence))
    )
    return sequence, total_movement, wrap_points
