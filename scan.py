def run_scan(requests, start, direction, max_cylinder):
    # Sort the list of cylinder requests in ascending order
    requests = sorted(requests)
    # Initialize total head movement to 0
    movement = 0
    # Sequence will track the order in which cylinders are serviced
    sequence = []
    # Set the current head position to the start value
    current = start

    if direction == 'right':
        # Requests to the right of or at the current position
        right = [r for r in requests if r >= start]
        # Requests to the left of the current position, reversed for servicing in order
        left = [r for r in requests if r < start][::-1]
        for r in right:
            # Add the request to the sequence
            sequence.append(r)
            # Add the distance moved to reach this request
            movement += abs(current - r)
            # Move the head to the current request
            current = r
        # Move to the end of the disk if not already there
        if current != max_cylinder:
            sequence.append(max_cylinder)
            movement += abs(current - max_cylinder)
            current = max_cylinder
        for r in left:
            # Service the remaining requests on the left in reverse order
            sequence.append(r)
            movement += abs(current - r)
            current = r
    else:
        # Requests to the left of or at the current position, reversed for servicing in order
        left = [r for r in requests if r <= start][::-1]
        # Requests to the right of the current position
        right = [r for r in requests if r > start]
        for r in left:
            # Add the request to the sequence
            sequence.append(r)
            # Add the distance moved to reach this request
            movement += abs(current - r)
            # Move the head to the current request
            current = r
        # Move to the beginning of the disk if not already there
        if current != 0:
            sequence.append(0)
            movement += abs(current - 0)
            current = 0
        for r in right:
            # Service the remaining requests on the right
            sequence.append(r)
            movement += abs(current - r)
            current = r

    # Return the sequence of serviced requests and the total movement
    return sequence, movement
