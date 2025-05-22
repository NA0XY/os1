1| def run_clook(requests, start, direction, max_cylinder):  # Define function for C-LOOK disk scheduling with arguments: requests (list), start (int), direction (str), max_cylinder (int)
2|     requests = sorted(requests)  # Sort the list of requested cylinders in ascending order
3|     movement = 0  # Initialize total head movement to zero
4|     sequence = []  # Initialize the sequence list to record the order of servicing requests
5|     current = start  # Set the current head position to the starting cylinder
6| 
7|     if direction == 'right':  # If the head is moving to the right (towards higher cylinder numbers)
8|         right = [r for r in requests if r >= start]  # List of requests to the right of or at the start position
9|         left = [r for r in requests if r < start]  # List of requests to the left of the start position
10|         for r in right:  # For each request on the right side
11|             sequence.append(r)  # Add the request to the service sequence
12|             movement += abs(current - r)  # Add the distance moved to reach this request
13|             current = r  # Update the current position
14|         if left:  # If there are requests on the left side
15|             movement += abs(current - left[0])  # Move the head directly to the leftmost unserviced request (simulate C-LOOK jump)
16|             current = left[0]  # Update the current position to the leftmost request
17|             for r in left:  # Service the remaining left-side requests
18|                 sequence.append(r)  # Add the request to the sequence
19|                 movement += abs(current - r)  # Add the distance moved
20|                 current = r  # Update the current position
21|     else:  # If the head is moving to the left (towards lower cylinder numbers)
22|         left = [r for r in requests if r <= start][::-1]  # Requests left of or at start, reversed for descending order
23|         right = [r for r in requests if r > start][::-1]  # Requests right of start, reversed for descending order
24|         for r in left:  # For each left-side request
25|             sequence.append(r)  # Add request to the sequence
26|             movement += abs(current - r)  # Move head and add distance
27|             current = r  # Update position
28|         if right:  # If there are right-side requests
29|             movement += abs(current - right[0])  # Jump to the rightmost unserviced request (C-LOOK jump)
30|             current = right[0]  # Update current position
31|             for r in right:  # Service remaining right-side requests
32|                 sequence.append(r)  # Add request to sequence
33|                 movement += abs(current - r)  # Add distance moved
34|                 current = r  # Update position
35| 
36|     return sequence, movement  # Return the service order and total head movement
37| 
