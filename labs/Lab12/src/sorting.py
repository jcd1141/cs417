"""
Lab 12: Breaking the O(n^2) Barrier

In this lab you will complete the core logic for three advanced
sorting algorithms: shell sort, merge sort, and quicksort.

The recursive structure and helper scaffolding are provided —
your job is to fill in the key mechanisms:
  - Shell sort: the gap insertion sort helper (Task 1)
  - Merge sort: the merge step (Task 2)
  - Quicksort: the partition (Task 3)

Counted versions are provided complete for use in the analysis
notebook.

Complete the THREE sections marked with TODO.
Do NOT change the function signatures or the provided code.

Run tests:
    pytest -v
"""


# ── TODO 1: Shell Sort — Gap Insertion Sort ───────────────────────


def _gap_insertion_sort(a_list, start, gap):
    """
    Perform insertion sort on a sublist defined by a starting
    position and gap.

    This sorts the elements at positions start, start+gap,
    start+2*gap, ... using insertion sort logic, but comparing
    and shifting by 'gap' positions instead of 1.

    Algorithm:
        1. Loop from start + gap to len(a_list), stepping by gap
        2. For each position i:
           - Save a_list[i] as current_value
           - Set position = i
           - Walk backward by gap: while position >= gap AND
             a_list[position - gap] > current_value:
               shift: a_list[position] = a_list[position - gap]
               position = position - gap
           - Place current_value at position

    This is your insertion sort from Lab 11, but every "1"
    becomes "gap". The while condition checks position >= gap
    (not position >= 0) because we step back by gap, not by 1.

    Args:
        a_list: The full list being sorted.
        start: The starting index of this sublist.
        gap: The distance between sublist elements.
    """
    pass  # TODO: implement this


def shell_sort(a_list):
    """
    Sort a_list in ascending order using Shell sort.

    DO NOT MODIFY — this function is complete.
    It calls your _gap_insertion_sort helper above.
    """
    gap = len(a_list) // 2
    while gap > 0:
        for start_position in range(gap):
            _gap_insertion_sort(a_list, start_position, gap)
        gap = gap // 2
    return a_list


# ── TODO 2: Merge Sort — The Merge Step ──────────────────────────


def merge_sort(a_list):
    """
    Sort a_list in ascending order using merge sort.

    The recursive structure is provided. Your job is to fill in
    the MERGE STEP where indicated — combining two sorted halves
    (left and right) back into a_list.

    The merge uses three index variables, all starting at 0:
      - i walks through the left half
      - j walks through the right half
      - k fills positions in a_list

    The merge has THREE loops:
      1. Main merge: while i < len(left) AND j < len(right)
         Compare left[i] and right[j]. Take the SMALLER one
         (use <= for stability) and put it at a_list[k].
         Advance whichever index you took from, and advance k.
      2. Left remainder: while i < len(left)
         Copy left[i] to a_list[k], advance both.
      3. Right remainder: while j < len(right)
         Copy right[j] to a_list[k], advance both.

    Args:
        a_list: A list of comparable items.

    Returns:
        The same list, now sorted in ascending order.
    """
    if len(a_list) <= 1:
        return a_list

    mid = len(a_list) // 2
    left = a_list[:mid]
    right = a_list[mid:]

    merge_sort(left)
    merge_sort(right)

    # ── MERGE STEP: fill in below ──────────────────────────
    # Combine the sorted left and right halves back into a_list.
    # Initialize: i = 0, j = 0, k = 0
    # Then write the three while loops described above.

    pass  # TODO: replace this with the merge logic

    return a_list


# ── TODO 3: Quicksort — The Partition ─────────────────────────────


def _partition(a_list, first, last):
    """
    Partition a_list[first..last] around a pivot value.

    Uses the first item as the pivot. Two markers scan inward:

    Algorithm:
        1. pivot_value = a_list[first]
        2. left_mark = first + 1, right_mark = last
        3. Use a boolean 'done' flag, loop while not done:
           a. Advance left_mark while left_mark <= right_mark
              AND a_list[left_mark] <= pivot_value
           b. Advance right_mark while left_mark <= right_mark
              AND a_list[right_mark] >= pivot_value
           c. If right_mark < left_mark: set done = True
           d. Otherwise: swap a_list[left_mark] and a_list[right_mark]
        4. Swap a_list[first] with a_list[right_mark]
           (puts pivot in its final position)
        5. Return right_mark

    Args:
        a_list: The list being sorted.
        first: Start index of the region to partition.
        last: End index of the region to partition.

    Returns:
        The index where the pivot ended up (the split point).
    """
    pass  # TODO: implement this


def _quick_sort_helper(a_list, first, last):
    """Recursive quicksort. DO NOT MODIFY."""
    if first < last:
        split_point = _partition(a_list, first, last)
        _quick_sort_helper(a_list, first, split_point - 1)
        _quick_sort_helper(a_list, split_point + 1, last)


def quick_sort(a_list):
    """
    Sort a_list in ascending order using quicksort.

    DO NOT MODIFY — this function is complete.
    It calls _quick_sort_helper, which calls your _partition.
    """
    if len(a_list) > 1:
        _quick_sort_helper(a_list, 0, len(a_list) - 1)
    return a_list


# ── Counted Versions (PROVIDED — use in the analysis notebook) ────


def merge_sort_counted(a_list):
    """
    Merge sort that also counts comparisons and data moves.

    Returns:
        (sorted_list, comparisons, data_moves)

    You do NOT need to modify this function.
    Use it in the analysis notebook to measure performance.
    """
    counts = [0, 0]  # [comparisons, data_moves]

    def _merge_sort(lst):
        if len(lst) > 1:
            mid = len(lst) // 2
            left = lst[:mid]
            right = lst[mid:]
            _merge_sort(left)
            _merge_sort(right)
            i = j = k = 0
            while i < len(left) and j < len(right):
                counts[0] += 1
                if left[i] <= right[j]:
                    lst[k] = left[i]
                    i += 1
                else:
                    lst[k] = right[j]
                    j += 1
                counts[1] += 1
                k += 1
            while i < len(left):
                lst[k] = left[i]
                counts[1] += 1
                i += 1
                k += 1
            while j < len(right):
                lst[k] = right[j]
                counts[1] += 1
                j += 1
                k += 1

    _merge_sort(a_list)
    return (a_list, counts[0], counts[1])


def quick_sort_counted(a_list):
    """
    Quicksort that also counts comparisons and exchanges.

    Returns:
        (sorted_list, comparisons, exchanges)

    You do NOT need to modify this function.
    Use it in the analysis notebook to measure performance.
    """
    counts = [0, 0]  # [comparisons, exchanges]

    def _partition(lst, first, last):
        pivot_value = lst[first]
        left_mark = first + 1
        right_mark = last
        done = False
        while not done:
            while left_mark <= right_mark and lst[left_mark] <= pivot_value:
                counts[0] += 1
                left_mark += 1
            while left_mark <= right_mark and lst[right_mark] >= pivot_value:
                counts[0] += 1
                right_mark -= 1
            if right_mark < left_mark:
                done = True
            else:
                lst[left_mark], lst[right_mark] = lst[right_mark], lst[left_mark]
                counts[1] += 1
        lst[first], lst[right_mark] = lst[right_mark], lst[first]
        counts[1] += 1
        return right_mark

    def _qs(lst, first, last):
        if first < last:
            sp = _partition(lst, first, last)
            _qs(lst, first, sp - 1)
            _qs(lst, sp + 1, last)

    if len(a_list) > 1:
        _qs(a_list, 0, len(a_list) - 1)
    return (a_list, counts[0], counts[1])
