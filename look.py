def run_look(requests, start, direction):
    # Sort the incoming disk requests in ascending order
    requests = sorted(requests)
    # Initialize total head movement to 0
    movement = 0
    # Initialize the sequence of serviced requests
    sequence = []
    # Set the current head position to the start value
    current = start

    if direction == 'right':
        # Requests to the right (greater than or equal to start)
        right = [r for r in requests if r >= start]
        # Requests to the left (less than start), reversed for LOOK algorithm
        left = [r for r in requests if r < start][::-1]
        # Serve all requests to the right first
        for r in right:
            sequence.append(r)  # Add request to the sequence
            movement += abs(current - r)  # Add movement distance
            current = r  # Move head to current request
        # Then serve all requests to the left
        for r in left:
            sequence.append(r)
            movement += abs(current - r)
            current = r
    else:
        # Requests to the left (less than or equal to start), reversed
        left = [r for r in requests if r <= start][::-1]
        # Requests to the right (greater than start)
        right = [r for r in requests if r > start]
        # Serve all requests to the left first
        for r in left:
            sequence.append(r)
            movement += abs(current - r)
            current = r
        # Then serve all requests to the right
        for r in right:
            sequence.append(r)
            movement += abs(current - r)
            current = r

    # Return the service sequence and the total movement
    return sequence, movement
