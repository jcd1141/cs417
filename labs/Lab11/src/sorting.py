"""
Lab 11: Sorting — Why Big-O Isn't the Whole Story

In this lab you will implement two sorting algorithms (bubble sort
and insertion sort), an optimized variant (short bubble sort), and
counted versions that track comparisons and data moves.

Complete the five functions marked with TODO.
Do NOT change the function signatures.

Run tests:
    pytest -v
"""


# ── TODO 1: Bubble Sort ─────────────────────────────────────────


def bubble_sort(a_list):
    """
    Sort a_list in ascending order using bubble sort.

    Makes multiple passes through the list, comparing adjacent items
    and swapping any pair that is out of order. After each pass, the
    next largest item has "bubbled" into its correct position at the end.

    Algorithm:
        1. Make n - 1 passes (outer loop, where n = len(a_list))
        2. On pass i, compare adjacent items from position 0
           up to position n - 1 - i
        3. If a_list[j] > a_list[j + 1], swap them

    Args:
        a_list: A list of comparable items.

    Returns:
        The same list, now sorted in ascending order.
    """
    pass  # TODO: implement this


# ── TODO 2: Short Bubble Sort ───────────────────────────────────


def short_bubble_sort(a_list):
    """
    Sort a_list using bubble sort with early termination.

    Works exactly like bubble_sort, but tracks whether any exchanges
    happened during each pass. If a complete pass makes no exchanges,
    the list is already sorted — stop immediately.

    Hint: Use a boolean flag. Set it to False at the start of each
    pass, set it to True whenever you swap. After the pass, check it.

    Args:
        a_list: A list of comparable items.

    Returns:
        The same list, now sorted in ascending order.
    """
    pass  # TODO: implement this


# ── TODO 3: Insertion Sort ──────────────────────────────────────


def insertion_sort(a_list):
    """
    Sort a_list in ascending order using insertion sort.

    Builds a sorted region from the left side of the list. For each
    new item, shift larger items to the right to make room, then
    insert the item in its correct position.

    Algorithm:
        1. Start at position 1 (position 0 is a sorted list of one)
        2. Save the current item as current_value
        3. Walk backward through the sorted region (position i-1 down to 0):
           - If a_list[position] > current_value, shift it right
             (copy it to position + 1)
           - Otherwise, stop — you've found the insertion point
        4. Place current_value at the insertion point

    Hint: Use a while loop for the backward walk. Check
    position >= 0 FIRST in the condition — think about why the
    order matters.

    Args:
        a_list: A list of comparable items.

    Returns:
        The same list, now sorted in ascending order.
    """
    pass  # TODO: implement this


# ── TODO 4: Counted Versions ────────────────────────────────────


def bubble_sort_counted(a_list):
    """
    Sort a_list using bubble sort, counting comparisons and exchanges.

    Works exactly like bubble_sort, but also counts:
    - comparisons: each time you check if a_list[j] > a_list[j+1]
    - exchanges: each time you swap two items (count the swap as 1)

    Args:
        a_list: A list of comparable items.

    Returns:
        A tuple (sorted_list, comparisons, exchanges) where:
            sorted_list: The sorted list.
            comparisons: Total number of item comparisons made.
            exchanges: Total number of swaps performed.

    Example:
        bubble_sort_counted([3, 1, 2])
        → ([1, 2, 3], 3, 2)
    """
    pass  # TODO: implement this


def insertion_sort_counted(a_list):
    """
    Sort a_list using insertion sort, counting comparisons and data moves.

    Works exactly like insertion_sort, but also counts:
    - comparisons: each time you check if a_list[position] > current_value
    - data_moves: each shift (moving an item right) counts as 1,
      and the final placement of current_value counts as 1

    Args:
        a_list: A list of comparable items.

    Returns:
        A tuple (sorted_list, comparisons, data_moves) where:
            sorted_list: The sorted list.
            comparisons: Total number of item comparisons made.
            data_moves: Total number of shifts + placements.

    Example:
        insertion_sort_counted([3, 1, 2])
        → ([1, 2, 3], 3, 4)
    """
    pass  # TODO: implement this
