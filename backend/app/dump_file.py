# from ast import List
# import time
# from typing import Tuple


'''
This code is a utility for checking if two time intervals overlap, especially useful for restaurant operating hours.
It includes functions to convert time objects to minutes, get non-wrapping intervals, and check for overlaps.
It is specifically for if we want to check if time intervals are crossing midnight.
# def to_minutes(t: time) -> int:
#     """Convert a time object to minutes since midnight."""
#     return t.hour * 60 + t.minute

# def get_intervals(start: time, end: time) -> List[Tuple[int, int]]:
#     """
#     Return a list of non-wrapping intervals (in minutes) for a given start and end time.
#     If the interval crosses midnight, it is split into two intervals.
#     """
#     start_min = to_minutes(start)
#     end_min = to_minutes(end)
#     if end_min <= start_min:
#         return [(start_min, 1440), (0, end_min)]
#     return [(start_min, end_min)]

# def check_timeframes(start1: time, end1: time, start2: time, end2: time) -> bool:
#     """
#     Returns True if the two timeframes do NOT overlap (they are separate), and False otherwise.
    
#     This function handles intervals crossing midnight by splitting any such interval into two parts.
    
#     Overlap is checked for each pair of subintervals:
#       If NOT (first_interval_end <= second_interval_start or second_interval_end <= first_interval_start)
#       then the subintervals overlap.
#     """
#     intervals1 = get_intervals(start1, end1)
#     intervals2 = get_intervals(start2, end2)
    
#     for s1, e1 in intervals1:
#         for s2, e2 in intervals2:
#             if not (e1 <= s2 or e2 <= s1):
#                 return False  # Overlap found
#     return True'''
