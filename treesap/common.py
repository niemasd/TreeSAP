#!/usr/bin/env python3
def check_end_conditions(end_num_leaves, end_time):
    if end_num_leaves == float('inf') and end_time == float('inf'):
        raise ValueError("Must specify either end_num_leaves or end_time (or both)")
    if end_num_leaves != float('inf') and not isinstance(end_num_leaves,int):
        raise TypeError("end_num_leaves must be an integer")
    elif end_num_leaves < 1:
        raise ValueError("end_num_leaves must be at least 1")
    if not isinstance(end_time,float) and not isinstance(end_time,int):
        raise TypeError("end_time must be a float")
    if end_time <= 0:
        raise ValueError("end_time must be positive")
