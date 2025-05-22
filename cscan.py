def run_cscan(requests, start, direction, max_cylinder):
    # Sort the list of requests in ascending order
    requests = sorted(requests)
    # Initialize total head movement to 0
    movement = 0
    # List to store the order in which the requests are serviced
    sequence = []
    # Set the current head position to the starting position
    current = start

    # If the scan direction is towards higher cylinder numbers
    if direction == 'right':
        # Requests greater than or equal to the starting position
        right = [r for r in requests if r >= start]
        # Requests less than the starting position
        left = [r for r in requests if r < start]
        # Service all requests to the right of the starting position
        for r in right:
            sequence.append(r)              # Add request to service sequence
            movement += abs(current - r)    # Add the distance moved to service this request
            current = r                     # Update the current head position
        # If not already at the end, go to the maximum cylinder
        if current != max_cylinder:
            sequence.append(max_cylinder)               # Go to the end of the disk
            movement += abs(current - max_cylinder)     # Add movement to end
            current = max_cylinder                      # Update head position
        # If there are requests on the left side
        if left:
            sequence.append(0)                # Move head to the start (cylinder 0)
            movement += abs(current - 0)      # Add movement to start
            current = 0                       # Update head position
            # Service all requests on the left side
            for r in left:
                sequence.append(r)            # Add request to service sequence
                movement += abs(current - r)  # Add distance moved
                current = r                   # Update head position
    else:
        # If scan direction is 'left', service requests to the left first (in descending order)
        left = [r for r in requests if r <= start][::-1]
        # Requests greater than the starting position (to be serviced after wrap)
        right = [r for r in requests if r > start][::-1]
        # Service all requests to the left of the starting position
        for r in left:
            sequence.append(r)              # Add request to service sequence
            movement += abs(current - r)    # Add distance moved
            current = r                     # Update head position
        # If not already at the beginning, move head to cylinder 0
        if current != 0:
            sequence.append(0)                # Go to the start of the disk
            movement += abs(current - 0)      # Add movement to start
            current = 0                       # Update head position
        # If there are requests on the right side
        if right:
            sequence.append(max_cylinder)               # Move head to max cylinder (wrap around)
            movement += abs(current - max_cylinder)     # Add movement
            current = max_cylinder                      # Update head position
            # Service all requests on the right side (in descending order)
            for r in right:
                sequence.append(r)            # Add request to service sequence
                movement += abs(current - r)  # Add distance moved
                current = r                   # Update head position

    # Return the servicing sequence and total head movement
    return sequence, movement
