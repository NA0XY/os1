def run_cscan(requests, start, direction, max_cylinder):
    requests = sorted(requests)
    movement = 0
    sequence = []
    current = start

    if direction == 'right':
        right = [r for r in requests if r >= start]
        left = [r for r in requests if r < start]
        for r in right:
            sequence.append(r)
            movement += abs(current - r)
            current = r
        if current != max_cylinder:
            sequence.append(max_cylinder)
            movement += abs(current - max_cylinder)
            current = max_cylinder
        if left:
            sequence.append(0)
            movement += abs(current - 0)
            current = 0
            for r in left:
                sequence.append(r)
                movement += abs(current - r)
                current = r
    else:
        left = [r for r in requests if r <= start][::-1]
        right = [r for r in requests if r > start][::-1]
        for r in left:
            sequence.append(r)
            movement += abs(current - r)
            current = r
        if current != 0:
            sequence.append(0)
            movement += abs(current - 0)
            current = 0
        if right:
            sequence.append(max_cylinder)
            movement += abs(current - max_cylinder)
            current = max_cylinder
            for r in right:
                sequence.append(r)
                movement += abs(current - r)
                current = r

    return sequence, movement
