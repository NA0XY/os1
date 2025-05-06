# cscan.py

def run_cscan(requests, start, direction='right', max_cylinder=199):
    if not requests:
        return [], 0, []

    requests = sorted(set(requests))
    left = [r for r in requests if r < start]
    right = [r for r in requests if r >= start]
    sequence = []
    wrap_moves = []

    if direction == 'right':
        sequence.extend(right)
        if right and right[-1] != max_cylinder:
            wrap_moves.append((right[-1], max_cylinder))
        wrap_moves.append((max_cylinder, 0))
        sequence.extend(left)
    elif direction == 'left':
        sequence.extend(reversed(left))
        if left and left[0] != 0:
            wrap_moves.append((left[0], 0))
        wrap_moves.append((0, max_cylinder))
        sequence.extend(reversed(right))
    else:
        raise ValueError("Direction must be 'right' or 'left'")

    full_sequence = [start] + sequence
    movement = 0
    pos = start
    for track in sequence:
        movement += abs(track - pos)
        pos = track

    return sequence, movement, wrap_moves
