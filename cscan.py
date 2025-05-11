# cscan.py

def run_cscan(requests, start, direction='right', max_cylinder=199):
    """
    Perform C-SCAN disk scheduling.

    Parameters:
    - requests: list of disk track numbers (integers)
    - start: initial head position
    - direction: 'right' or 'left'
    - max_cylinder: highest track number on the disk

    Returns:
    - sequence: list of serviced disk tracks
    - movement: total head movement
    """
    if not requests:
        return [], 0

    # Remove duplicates and sort
    requests = sorted(set(requests))
    left  = [r for r in requests if r < start]
    right = [r for r in requests if r >= start]

    sequence = []
    if direction == 'right':
        sequence.extend(right)
        if right and right[-1] != max_cylinder:
            sequence.append(max_cylinder)  # Go to end (but don't show it in sequence)
        sequence.append(0)                 # Wrap to start (but don't show it)
        sequence.extend(left)
    elif direction == 'left':
        sequence.extend(reversed(left))
        if left and left[0] != 0:
            sequence.append(0)             # Go to start (but don't show it)
        sequence.append(max_cylinder)      # Wrap to end (but don't show it)
        sequence.extend(reversed(right))
    else:
        raise ValueError("Direction must be 'right' or 'left'")

    # Clean up the sequence to remove 0 and max_cylinder
    sequence = [track for track in sequence if track != 0 and track != max_cylinder]

    movement = 0
    pos = start
    for track in sequence:
        movement += abs(track - pos)
        pos = track

    return sequence, movement
