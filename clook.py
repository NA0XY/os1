def run_clook(requests, start, direction, max_cylinder):
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
        if left:
            movement += abs(current - left[0])
            current = left[0]
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
        if right:
            movement += abs(current - right[0])
            current = right[0]
            for r in right:
                sequence.append(r)
                movement += abs(current - r)
                current = r

    return sequence, movement
