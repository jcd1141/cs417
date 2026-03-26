"""
Tests for Lab 15: Priority in Practice — Heaps and heapq

Run: pytest -v
"""

import pytest
from heap_basics import push_and_pop, heapify_and_peek, top_k_smallest, sort_by_priority
from scheduler import TaskScheduler


# ── Task 1: Heap Basics ─────────────────────────────────────────────

class TestHeapBasics:
    """Basic heapq operations: push/pop, heapify, top-k."""

    def test_push_and_pop_returns_sorted(self):
        result = push_and_pop([5, 1, 8, 3, 2])
        assert result == [1, 2, 3, 5, 8]

    def test_push_and_pop_single(self):
        assert push_and_pop([42]) == [42]

    def test_push_and_pop_already_sorted(self):
        result = push_and_pop([1, 2, 3, 4, 5])
        assert result == [1, 2, 3, 4, 5]

    def test_push_and_pop_duplicates(self):
        result = push_and_pop([3, 1, 3, 1, 2])
        assert result == [1, 1, 2, 3, 3]

    def test_push_and_pop_empty(self):
        assert push_and_pop([]) == []

    def test_heapify_and_peek(self):
        assert heapify_and_peek([5, 1, 8, 3, 2]) == 1

    def test_heapify_and_peek_single(self):
        assert heapify_and_peek([7]) == 7

    def test_heapify_and_peek_negative(self):
        assert heapify_and_peek([3, -1, 5, 0]) == -1

    def test_top_k_smallest(self):
        result = top_k_smallest([10, 4, 7, 1, 3, 9, 2], 3)
        assert result == [1, 2, 3]

    def test_top_k_smallest_k_equals_length(self):
        result = top_k_smallest([5, 3, 1], 3)
        assert result == [1, 3, 5]

    def test_top_k_smallest_k_is_one(self):
        result = top_k_smallest([8, 2, 6, 4], 1)
        assert result == [2]


# ── Task 2: Tuple Priorities ────────────────────────────────────────

class TestTuplePriorities:
    """Priority sorting with tuple heaps and FIFO tiebreaking."""

    def test_different_priorities(self):
        tasks = [(3, "low"), (1, "high"), (2, "medium")]
        assert sort_by_priority(tasks) == ["high", "medium", "low"]

    def test_same_priority_fifo(self):
        tasks = [(1, "first"), (1, "second"), (1, "third")]
        assert sort_by_priority(tasks) == ["first", "second", "third"]

    def test_mixed_priorities_with_ties(self):
        tasks = [
            (3, "update docs"),
            (1, "server down"),
            (1, "database down"),
            (2, "fix bug"),
        ]
        result = sort_by_priority(tasks)
        assert result == ["server down", "database down", "fix bug", "update docs"]

    def test_single_task(self):
        assert sort_by_priority([(5, "only one")]) == ["only one"]

    def test_empty(self):
        assert sort_by_priority([]) == []


# ── Task 3: TaskScheduler ───────────────────────────────────────────

class TestTaskScheduler:
    """Full scheduler: add, next, peek, len, is_empty."""

    def test_basic_priority_order(self):
        s = TaskScheduler()
        s.add_task(2, "fix login bug")
        s.add_task(1, "server is down")
        s.add_task(3, "update docs")
        assert s.next_task() == "server is down"
        assert s.next_task() == "fix login bug"
        assert s.next_task() == "update docs"

    def test_fifo_within_same_priority(self):
        s = TaskScheduler()
        s.add_task(1, "first")
        s.add_task(1, "second")
        s.add_task(1, "third")
        assert s.next_task() == "first"
        assert s.next_task() == "second"
        assert s.next_task() == "third"

    def test_peek_does_not_remove(self):
        s = TaskScheduler()
        s.add_task(1, "important")
        assert s.peek() == "important"
        assert s.peek() == "important"
        assert len(s) == 1

    def test_next_task_empty_returns_none(self):
        s = TaskScheduler()
        assert s.next_task() is None

    def test_peek_empty_returns_none(self):
        s = TaskScheduler()
        assert s.peek() is None

    def test_len(self):
        s = TaskScheduler()
        assert len(s) == 0
        s.add_task(1, "a")
        assert len(s) == 1
        s.add_task(2, "b")
        assert len(s) == 2
        s.next_task()
        assert len(s) == 1

    def test_is_empty(self):
        s = TaskScheduler()
        assert s.is_empty() is True
        s.add_task(1, "task")
        assert s.is_empty() is False
        s.next_task()
        assert s.is_empty() is True

    def test_interleaved_add_and_next(self):
        """Tasks arriving while others are being processed."""
        s = TaskScheduler()
        s.add_task(2, "medium task")
        s.add_task(3, "low task")
        assert s.next_task() == "medium task"

        # New urgent task arrives mid-processing
        s.add_task(1, "urgent task")
        assert s.next_task() == "urgent task"
        assert s.next_task() == "low task"

    def test_many_priorities(self):
        s = TaskScheduler()
        s.add_task(5, "e")
        s.add_task(3, "c")
        s.add_task(1, "a")
        s.add_task(4, "d")
        s.add_task(2, "b")
        result = [s.next_task() for _ in range(5)]
        assert result == ["a", "b", "c", "d", "e"]