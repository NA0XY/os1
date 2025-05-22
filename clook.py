def run_clook(requests, start, direction, max_cylinder):  # Define function for C-LOOK disk scheduling with arguments: requests (list), start (int), direction (str), max_cylinder (int)
    requests = sorted(requests)  # Sort the list of requested cylinders in ascending order
    movement = 0  # Initialize total head movement to zero
    sequence = []  # Initialize the sequence list to record the order of servicing requests
    current = start  # Set the current head position to the starting cylinder

    if direction == 'right':  # If the head is moving to the right (towards higher cylinder numbers)
        right = [r for r in requests if r >= start]  # List of requests to the right of or at the start position
        left = [r for r in requests if r < start]  # List of requests to the left of the start position
        for r in right:  # For each request on the right side
            sequence.append(r)  # Add the request to the service sequence
            movement += abs(current - r)  # Add the distance moved to reach this request
            current = r  # Update the current position
        if left:  # If there are requests on the left side
            movement += abs(current - left[0])  # Move the head directly to the leftmost unserviced request (simulate C-LOOK jump)
            current = left[0]  # Update the current position to the leftmost request
            for r in left:  # Service the remaining left-side requests
                sequence.append(r)  # Add the request to the sequence
                movement += abs(current - r)  # Add the distance moved
                current = r  # Update the current position
    else:  # If the head is moving to the left (towards lower cylinder numbers)
        left = [r for r in requests if r <= start][::-1]  # Requests left of or at start, reversed for descending order
        right = [r for r in requests if r > start][::-1]  # Requests right of start, reversed for descending order
        for r in left:  # For each left-side request
            sequence.append(r)  # Add request to the sequence
            movement += abs(current - r)  # Move head and add distance
            current = r  # Update position
        if right:  # If there are right-side requests
            movement += abs(current - right[0])  # Jump to the rightmost unserviced request (C-LOOK jump)
            current = right[0]  # Update current position
            for r in right:  # Service remaining right-side requests
                sequence.append(r)  # Add request to sequence
                movement += abs(current - r)  # Add distance moved
                current = r  # Update position

    return sequence, movement  # Return the service order and total head movement
