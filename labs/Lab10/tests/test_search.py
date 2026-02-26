"""
Tests for Searching Lab — Lab 10.
Do not modify this file.

Run from the Lab10 directory:
    pytest -v
"""

from search import (
    sequential_search,
    binary_search,
    sequential_search_counted,
    binary_search_counted,
)


# ═══════════════════════════════════════════════════════════════════
# Task 1 Tests: Sequential Search
# ═══════════════════════════════════════════════════════════════════


class TestSequentialSearch:
    """Tests for sequential (linear) search."""

    def test_find_first_item(self):
        assert sequential_search([10, 20, 30, 40, 50], 10) is True

    def test_find_last_item(self):
        assert sequential_search([10, 20, 30, 40, 50], 50) is True

    def test_find_middle_item(self):
        assert sequential_search([10, 20, 30, 40, 50], 30) is True

    def test_not_found(self):
        assert sequential_search([10, 20, 30, 40, 50], 99) is False

    def test_empty_list(self):
        assert sequential_search([], 5) is False

    def test_single_item_found(self):
        assert sequential_search([42], 42) is True

    def test_single_item_not_found(self):
        assert sequential_search([42], 7) is False

    def test_duplicates(self):
        """Finding an item that appears multiple times still returns True."""
        assert sequential_search([3, 7, 3, 9, 3], 3) is True

    def test_unsorted_list(self):
        """Sequential search works on unsorted lists."""
        assert sequential_search([8, 2, 5, 1, 9, 3], 5) is True


# ═══════════════════════════════════════════════════════════════════
# Task 2 Tests: Binary Search
# ═══════════════════════════════════════════════════════════════════


class TestBinarySearch:
    """Tests for binary search on sorted lists."""

    def test_find_first_item(self):
        assert binary_search([10, 20, 30, 40, 50], 10) is True

    def test_find_last_item(self):
        assert binary_search([10, 20, 30, 40, 50], 50) is True

    def test_find_middle_item(self):
        assert binary_search([10, 20, 30, 40, 50], 30) is True

    def test_not_found_between(self):
        """Target falls between two existing items."""
        assert binary_search([10, 20, 30, 40, 50], 25) is False

    def test_not_found_below(self):
        """Target is smaller than every item."""
        assert binary_search([10, 20, 30, 40, 50], 5) is False

    def test_not_found_above(self):
        """Target is larger than every item."""
        assert binary_search([10, 20, 30, 40, 50], 99) is False

    def test_empty_list(self):
        assert binary_search([], 5) is False

    def test_single_item_found(self):
        assert binary_search([42], 42) is True

    def test_single_item_not_found(self):
        assert binary_search([42], 7) is False

    def test_two_items_find_first(self):
        assert binary_search([10, 20], 10) is True

    def test_two_items_find_second(self):
        assert binary_search([10, 20], 20) is True

    def test_two_items_not_found(self):
        assert binary_search([10, 20], 15) is False

    def test_even_length_list(self):
        assert binary_search([2, 4, 6, 8, 10, 12], 8) is True

    def test_odd_length_list(self):
        assert binary_search([1, 3, 5, 7, 9], 7) is True

    def test_large_sorted_list(self):
        """Binary search works correctly on a larger list."""
        big_list = list(range(0, 1000, 2))  # [0, 2, 4, ..., 998]
        assert binary_search(big_list, 500) is True
        assert binary_search(big_list, 501) is False


# ═══════════════════════════════════════════════════════════════════
# Task 3 Tests: Counted Versions
# ═══════════════════════════════════════════════════════════════════


class TestCounted:
    """Tests for comparison-counting search functions."""

    # ── Sequential counted ──

    def test_sequential_counted_found(self):
        found, count = sequential_search_counted([4, 8, 2, 15, 17], 17)
        assert found is True
        assert count == 5  # target is the last item

    def test_sequential_counted_not_found(self):
        found, count = sequential_search_counted([4, 8, 2, 15, 17], 99)
        assert found is False
        assert count == 5  # checked every item

    def test_sequential_counted_first_item(self):
        found, count = sequential_search_counted([4, 8, 2, 15, 17], 4)
        assert found is True
        assert count == 1  # found immediately

    def test_sequential_counted_empty(self):
        found, count = sequential_search_counted([], 5)
        assert found is False
        assert count == 0

    # ── Binary counted ──

    def test_binary_counted_found(self):
        found, count = binary_search_counted([2, 4, 8, 15, 17], 8)
        assert found is True
        assert count == 1  # 8 is the midpoint

    def test_binary_counted_not_found(self):
        found, count = binary_search_counted([2, 4, 8, 15, 17], 99)
        assert found is False
        assert count > 0

    def test_binary_counted_empty(self):
        found, count = binary_search_counted([], 5)
        assert found is False
        assert count == 0

    def test_binary_fewer_than_sequential(self):
        """Binary search should use fewer comparisons on a large sorted list."""
        big_list = list(range(1000))
        _, seq_count = sequential_search_counted(big_list, 999)
        _, bin_count = binary_search_counted(big_list, 999)
        assert bin_count < seq_count

    def test_binary_counted_max_comparisons(self):
        """On a 1000-element list, binary search should use at most ~10 comparisons."""
        big_list = list(range(1000))
        _, count = binary_search_counted(big_list, -1)  # not found
        assert count <= 11  # ceil(log2(1000)) = 10, allow 1 margin
