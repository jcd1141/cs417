"""
Lab 10: Searching — From Linear Scan to Divide and Conquer

In this lab you will implement two search algorithms and then
create versions that count comparisons so you can measure
their performance.

Complete the four functions marked with TODO.
Do NOT change the function signatures.

Run tests:
    pytest -v
"""


# ── TODO 1: Sequential Search ────────────────────────────────────


def sequential_search(a_list, target):
    """
    Search for target in a_list by checking each item from the start.

    Args:
        a_list: A list of items (not necessarily sorted).
        target: The item to search for.

    Returns:
        True if target is found, False otherwise.
    """
    # TODO: implement this
    for i in a_list:
        if i == target:
            return True

    return False


# ── TODO 2: Binary Search ────────────────────────────────────────


def binary_search(a_list, target):
    """
    Search for target in a sorted list by repeatedly halving
    the search space.

    The list MUST be sorted in ascending order for this to work.

    Algorithm:
        1. Set first = 0, last = len(a_list) - 1
        2. While first <= last:
           - Compute mid = (first + last) // 2
           - If a_list[mid] == target → return True
           - If target < a_list[mid] → search the left half (last = mid - 1)
           - If target > a_list[mid] → search the right half (first = mid + 1)
        3. If the loop ends → return False

    Args:
        a_list: A sorted list of items.
        target: The item to search for.

    Returns:
        True if target is found, False otherwise.
    """
    # TODO: implement this
    first = 0
    last = len(a_list) - 1

    while first <= last:
        middle = (first + last) // 2
        if a_list[middle] == target:
            return True
        elif target < a_list[middle]:
            last = middle - 1
        else:
            first = middle + 1

    return False


# ── TODO 3: Counted Versions ─────────────────────────────────────


def sequential_search_counted(a_list, target):
    """
    Same as sequential_search, but also counts comparisons.

    A "comparison" is each time you check whether a list element
    equals the target.

    Args:
        a_list: A list of items (not necessarily sorted).
        target: The item to search for.

    Returns:
        A tuple (found, comparisons) where:
            found: True if target is in the list, False otherwise.
            comparisons: The number of element-to-target comparisons made.

    Example:
        sequential_search_counted([4, 8, 2, 15, 17], 17)  → (True, 5)
        sequential_search_counted([4, 8, 2, 15, 17], 99)  → (False, 5)
    """
    # TODO: implement this
    comp = 0

    for i in a_list:
        comp += 1
        if i == target:
            return (True, comp)
        
    return (False, comp)

def binary_search_counted(a_list, target):
    """
    Same as binary_search, but also counts comparisons.

    A "comparison" is each time you check a_list[mid] against the target.
    Count one comparison per loop iteration (the mid check).

    Args:
        a_list: A sorted list of items.
        target: The item to search for.

    Returns:
        A tuple (found, comparisons) where:
            found: True if target is in the list, False otherwise.
            comparisons: The number of midpoint-to-target comparisons made.

    Example:
        binary_search_counted([2, 4, 8, 15, 17], 17)  → (True, 3)
        binary_search_counted([2, 4, 8, 15, 17], 99)  → (False, 3)
    """
    # TODO: implement this
    comp = 0
    first = 0
    last = len(a_list) - 1

    while first <= last:
        middle = (first + last) // 2
        comp +=1
        if a_list[middle] == target:
            return (True, comp)
        elif target < a_list[middle]:
            last = middle - 1
        else:
            first = middle + 1

    return (False, comp)
