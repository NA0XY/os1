def run_scan(requests, start, direction='right'):
    if not requests:
        return [], 0

    requests = sorted(requests)
    left = [r for r in requests if r < start]
    right = [r for r in requests if r >= start]

    sequence = []
    if direction == 'right':
        sequence = right + left[::-1]
    elif direction == 'left':
        sequence = left[::-1] + right
    else:
        raise ValueError("Direction must be 'left' or 'right'")

    total_movement = 0
    current = start
    for track in sequence:
        total_movement += abs(current - track)
        current = track

    return sequence, total_movement
