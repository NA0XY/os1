def run_scan(requests, start, direction='right'):
    if not requests:
        return [], 0
    requests = sorted(requests)
    left = [r for r in requests if r < start]
    right = [r for r in requests if r >= start]
    if direction == 'right':
        sequence = right + left[::-1]
    else:
        sequence = left[::-1] + right
    movement = 0
    pos = start
    for track in sequence:
        movement += abs(pos - track)
        pos = track
    return sequence, movement
