def run_cscan(requests, start, direction='right', max_cylinder=199):
    if not requests:
        return [], 0
    requests = sorted(set(requests))
    left = [r for r in requests if r < start]
    right = [r for r in requests if r >= start]
    sequence = []
    if direction == 'right':
        sequence.extend(right)
        if right and right[-1] != max_cylinder:
            sequence.append(max_cylinder)
        sequence.append(0)
        sequence.extend(left)
    else:
        sequence.extend(reversed(left))
        if left and left[0] != 0:
            sequence.append(0)
        sequence.append(max_cylinder)
        sequence.extend(reversed(right))
    sequence = [track for track in sequence if track not in [0, max_cylinder]]
    movement = 0
    pos = start
    for track in sequence:
        movement += abs(track - pos)
        pos = track
    return sequence, movement
