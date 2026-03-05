"""
Tests for Sorting Lab — Lab 12.
Do not modify this file.

Run from the Lab12 directory:
    pytest -v
"""

from sorting import (
    shell_sort,
    merge_sort,
    quick_sort,
    merge_sort_counted,
    quick_sort_counted,
)


# ===================================================================
# Task 1 Tests: Shell Sort
# ===================================================================


class TestShellSort:
    """Tests for Shell sort (via your _gap_insertion_sort helper)."""

    def test_basic_sort(self):
        assert shell_sort([54, 26, 93, 17, 77]) == [17, 26, 54, 77, 93]

    def test_already_sorted(self):
        assert shell_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert shell_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_duplicates(self):
        assert shell_sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]

    def test_single_item(self):
        assert shell_sort([42]) == [42]

    def test_empty_list(self):
        assert shell_sort([]) == []

    def test_two_items(self):
        assert shell_sort([7, 3]) == [3, 7]

    def test_all_same(self):
        assert shell_sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    def test_sorts_in_place(self):
        """shell_sort should modify and return the original list."""
        original = [3, 1, 2]
        result = shell_sort(original)
        assert result is original
        assert result == [1, 2, 3]

    def test_negative_numbers(self):
        assert shell_sort([3, -1, 4, -5, 2]) == [-5, -1, 2, 3, 4]

    def test_large_list(self):
        """Verify correctness on a larger input."""
        import random
        data = list(range(200))
        random.shuffle(data)
        assert shell_sort(data) == list(range(200))


# ===================================================================
# Task 2 Tests: Merge Sort
# ===================================================================


class TestMergeSort:
    """Tests for merge sort (via your merge step)."""

    def test_basic_sort(self):
        assert merge_sort([54, 26, 93, 17, 77]) == [17, 26, 54, 77, 93]

    def test_already_sorted(self):
        assert merge_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_duplicates(self):
        assert merge_sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]

    def test_single_item(self):
        assert merge_sort([42]) == [42]

    def test_empty_list(self):
        assert merge_sort([]) == []

    def test_two_items(self):
        assert merge_sort([7, 3]) == [3, 7]

    def test_all_same(self):
        assert merge_sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    def test_sorts_in_place(self):
        """merge_sort should modify and return the original list."""
        original = [3, 1, 2]
        result = merge_sort(original)
        assert result is original
        assert result == [1, 2, 3]

    def test_negative_numbers(self):
        assert merge_sort([3, -1, 4, -5, 2]) == [-5, -1, 2, 3, 4]

    def test_large_list(self):
        """Verify correctness on a larger input."""
        import random
        data = list(range(200))
        random.shuffle(data)
        assert merge_sort(data) == list(range(200))


# ===================================================================
# Task 3 Tests: Quicksort
# ===================================================================


class TestQuickSort:
    """Tests for quicksort (via your _partition function)."""

    def test_basic_sort(self):
        assert quick_sort([54, 26, 93, 17, 77]) == [17, 26, 54, 77, 93]

    def test_already_sorted(self):
        assert quick_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_duplicates(self):
        assert quick_sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]

    def test_single_item(self):
        assert quick_sort([42]) == [42]

    def test_empty_list(self):
        assert quick_sort([]) == []

    def test_two_items(self):
        assert quick_sort([7, 3]) == [3, 7]

    def test_two_items_already_sorted(self):
        assert quick_sort([3, 7]) == [3, 7]

    def test_all_same(self):
        assert quick_sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    def test_sorts_in_place(self):
        """quick_sort should modify and return the original list."""
        original = [3, 1, 2]
        result = quick_sort(original)
        assert result is original
        assert result == [1, 2, 3]

    def test_negative_numbers(self):
        assert quick_sort([3, -1, 4, -5, 2]) == [-5, -1, 2, 3, 4]

    def test_large_list(self):
        """Verify correctness on a larger input."""
        import random
        data = list(range(200))
        random.shuffle(data)
        assert quick_sort(data) == list(range(200))


# ===================================================================
# Provided Counted Versions — Smoke Tests
# ===================================================================


class TestCountedSmoke:
    """Basic smoke tests for the provided counted versions.
    These verify the counted functions work correctly so you
    can trust them in the analysis notebook."""

    def test_merge_counted_produces_sorted_output(self):
        result, comps, moves = merge_sort_counted([54, 26, 93, 17, 77])
        assert result == [17, 26, 54, 77, 93]
        assert comps > 0
        assert moves > 0

    def test_quick_counted_produces_sorted_output(self):
        result, comps, exchanges = quick_sort_counted([54, 26, 93, 17, 77])
        assert result == [17, 26, 54, 77, 93]
        assert comps > 0
        assert exchanges > 0

    def test_counted_versions_agree(self):
        """Both counted versions should produce the same sorted result."""
        import random
        data = list(range(100))
        random.seed(417)
        random.shuffle(data)

        m_result, _, _ = merge_sort_counted(data[:])
        q_result, _, _ = quick_sort_counted(data[:])
        assert m_result == q_result == sorted(data)
