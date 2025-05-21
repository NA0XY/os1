def run_cscan(requests, start, direction, max_cylinder):
    requests = sorted(requests)
    movement = 0
    sequence = []
    current = start

    if direction == 'right':
        right = [r for r in requests if r >= start]
        left = [r for r in requests if r < start]
        # Service right
        for r in right:
            sequence.append(r)
            movement += abs(current - r)
            current = r
        # Go to end if not already there
        if current != max_cylinder:
            sequence.append(max_cylinder)
            movement += abs(current - max_cylinder)
            current = max_cylinder
        # Jump to start (0)
        if left:
            sequence.append(0)
            movement += abs(current - 0)
            current = 0
            # Service left
            for r in left:
                sequence.append(r)
                movement += abs(current - r)
                current = r
    else:
        left = [r for r in requests if r <= start][::-1]
        right = [r for r in requests if r > start][::-1]
        # Service left
        for r in left:
            sequence.append(r)
            movement += abs(current - r)
            current = r
        # Go to start if not already there
        if current != 0:
            sequence.append(0)
            movement += abs(current - 0)
            current = 0
        # Jump to end (max_cylinder)
        if right:
            sequence.append(max_cylinder)
            movement += abs(current - max_cylinder)
            current = max_cylinder
            # Service right
            for r in right:
                sequence.append(r)
                movement += abs(current - r)
                current = r

    return sequence, movement