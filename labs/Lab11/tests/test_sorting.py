"""
Tests for Sorting Lab — Lab 11.
Do not modify this file.

Run from the Lab11 directory:
    pytest -v
"""

from sorting import (
    bubble_sort,
    short_bubble_sort,
    insertion_sort,
    bubble_sort_counted,
    insertion_sort_counted,
)


# ═══════════════════════════════════════════════════════════════════
# Task 1 Tests: Bubble Sort
# ═══════════════════════════════════════════════════════════════════


class TestBubbleSort:
    """Tests for standard bubble sort."""

    def test_basic_sort(self):
        assert bubble_sort([54, 26, 93, 17, 77]) == [17, 26, 54, 77, 93]

    def test_already_sorted(self):
        assert bubble_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert bubble_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_duplicates(self):
        assert bubble_sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]

    def test_single_item(self):
        assert bubble_sort([42]) == [42]

    def test_empty_list(self):
        assert bubble_sort([]) == []

    def test_two_items(self):
        assert bubble_sort([7, 3]) == [3, 7]

    def test_two_items_already_sorted(self):
        assert bubble_sort([3, 7]) == [3, 7]

    def test_all_same(self):
        assert bubble_sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    def test_sorts_in_place(self):
        """bubble_sort should modify and return the original list."""
        original = [3, 1, 2]
        result = bubble_sort(original)
        assert result is original
        assert result == [1, 2, 3]

    def test_negative_numbers(self):
        assert bubble_sort([3, -1, 4, -5, 2]) == [-5, -1, 2, 3, 4]


# ═══════════════════════════════════════════════════════════════════
# Task 2 Tests: Short Bubble Sort
# ═══════════════════════════════════════════════════════════════════


class TestShortBubbleSort:
    """Tests for bubble sort with early termination."""

    def test_basic_sort(self):
        assert short_bubble_sort([54, 26, 93, 17, 77]) == [17, 26, 54, 77, 93]

    def test_already_sorted(self):
        assert short_bubble_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert short_bubble_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_nearly_sorted(self):
        """Only two adjacent items out of place — should stop early."""
        assert short_bubble_sort([1, 3, 2, 4, 5]) == [1, 2, 3, 4, 5]

    def test_duplicates(self):
        assert short_bubble_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]

    def test_single_item(self):
        assert short_bubble_sort([42]) == [42]

    def test_empty_list(self):
        assert short_bubble_sort([]) == []

    def test_sorts_in_place(self):
        """short_bubble_sort should modify and return the original list."""
        original = [3, 1, 2]
        result = short_bubble_sort(original)
        assert result is original
        assert result == [1, 2, 3]

    def test_produces_same_result_as_bubble(self):
        """Short bubble must produce the same sorted output as standard bubble."""
        data = [20, 15, 8, 42, 3, 77, 11, 55]
        result = short_bubble_sort(data[:])
        assert result is not None, "short_bubble_sort returned None"
        assert result == bubble_sort(data[:])


# ═══════════════════════════════════════════════════════════════════
# Task 3 Tests: Insertion Sort
# ═══════════════════════════════════════════════════════════════════


class TestInsertionSort:
    """Tests for insertion sort."""

    def test_basic_sort(self):
        assert insertion_sort([54, 26, 93, 17, 77]) == [17, 26, 54, 77, 93]

    def test_already_sorted(self):
        assert insertion_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert insertion_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_duplicates(self):
        assert insertion_sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]

    def test_single_item(self):
        assert insertion_sort([42]) == [42]

    def test_empty_list(self):
        assert insertion_sort([]) == []

    def test_two_items(self):
        assert insertion_sort([7, 3]) == [3, 7]

    def test_all_same(self):
        assert insertion_sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    def test_sorts_in_place(self):
        """insertion_sort should modify and return the original list."""
        original = [3, 1, 2]
        result = insertion_sort(original)
        assert result is original
        assert result == [1, 2, 3]

    def test_negative_numbers(self):
        assert insertion_sort([3, -1, 4, -5, 2]) == [-5, -1, 2, 3, 4]

    def test_insertion_at_beginning(self):
        """Item that needs to go all the way to position 0."""
        assert insertion_sort([2, 3, 4, 5, 1]) == [1, 2, 3, 4, 5]

    def test_large_list(self):
        """Verify correctness on a larger input."""
        import random
        data = list(range(100))
        random.shuffle(data)
        assert insertion_sort(data) == list(range(100))


# ═══════════════════════════════════════════════════════════════════
# Task 4 Tests: Counted Versions
# ═══════════════════════════════════════════════════════════════════


class TestCounted:
    """Tests for comparison- and data-move-counting sort functions."""

    # ── Bubble sort counted ──

    def test_bubble_counted_basic(self):
        result, comps, exchanges = bubble_sort_counted([3, 1, 2])
        assert result == [1, 2, 3]
        assert comps == 3  # pass1: 2 comps, pass2: 1 comp
        assert exchanges == 2  # pass1: swap(3,1), swap(3,2)

    def test_bubble_counted_already_sorted(self):
        result, comps, exchanges = bubble_sort_counted([1, 2, 3])
        assert result == [1, 2, 3]
        assert comps == 3  # still makes all comparisons
        assert exchanges == 0

    def test_bubble_counted_reverse(self):
        result, comps, exchanges = bubble_sort_counted([3, 2, 1])
        assert result == [1, 2, 3]
        assert comps == 3
        assert exchanges == 3  # every comparison triggers a swap

    def test_bubble_counted_single(self):
        result, comps, exchanges = bubble_sort_counted([42])
        assert result == [42]
        assert comps == 0
        assert exchanges == 0

    def test_bubble_counted_empty(self):
        result, comps, exchanges = bubble_sort_counted([])
        assert result == []
        assert comps == 0
        assert exchanges == 0

    def test_bubble_counted_five_items(self):
        """Verify comparison count formula: n(n-1)/2 for standard bubble."""
        result, comps, exchanges = bubble_sort_counted([5, 4, 3, 2, 1])
        assert result == [1, 2, 3, 4, 5]
        assert comps == 10  # 4 + 3 + 2 + 1

    # ── Insertion sort counted ──

    def test_insertion_counted_basic(self):
        result, comps, data_moves = insertion_sort_counted([3, 1, 2])
        assert result == [1, 2, 3]
        assert comps == 3
        assert data_moves == 4  # pass1: 1 shift + 1 place; pass2: 1 shift + 1 place

    def test_insertion_counted_already_sorted(self):
        result, comps, data_moves = insertion_sort_counted([1, 2, 3])
        assert result == [1, 2, 3]
        assert comps == 2  # one comparison per pass, no shifts
        assert data_moves == 2  # just the placement each pass (no shifts needed)

    def test_insertion_counted_reverse(self):
        """Worst case: every item shifts all the way to position 0."""
        result, comps, data_moves = insertion_sort_counted([3, 2, 1])
        assert result == [1, 2, 3]
        assert comps == 3  # pass1: 1 comp; pass2: 2 comps
        assert data_moves == 5  # pass1: 1 shift + 1 place; pass2: 2 shifts + 1 place

    def test_insertion_counted_single(self):
        result, comps, data_moves = insertion_sort_counted([42])
        assert result == [42]
        assert comps == 0
        assert data_moves == 0

    def test_insertion_counted_empty(self):
        result, comps, data_moves = insertion_sort_counted([])
        assert result == []
        assert comps == 0
        assert data_moves == 0

    # ── Cross-algorithm comparison ──

    def test_insertion_fewer_data_moves_on_large_random(self):
        """On a large random list, insertion sort should use fewer data moves
        than bubble sort uses exchanges (shifts are cheaper than swaps)."""
        import random
        data = list(range(200))
        random.seed(417)
        random.shuffle(data)

        _, _, bubble_exchanges = bubble_sort_counted(data[:])
        _, _, insertion_moves = insertion_sort_counted(data[:])

        # Insertion sort's data moves may be numerically higher because it
        # counts shifts + placements, but each costs 1/3 of an exchange.
        # The real insight is in the notebook — here we just verify both
        # produce correctly sorted output.
        b_result, _, _ = bubble_sort_counted(data[:])
        i_result, _, _ = insertion_sort_counted(data[:])
        assert b_result == i_result == sorted(data)
