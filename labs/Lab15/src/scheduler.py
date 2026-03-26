"""
Lab 15: Task Scheduler — A priority queue in action

Task 3: Build a TaskScheduler class using heapq.
"""

import heapq


class TaskScheduler:
    """A priority-based task scheduler.

    Tasks are added with a priority (lower number = more urgent).
    Tasks with the same priority are processed in FIFO order.
    """

    def __init__(self):
        """Initialize the scheduler."""
        # TODO: Set up your internal data structures
        self.heap = []
        self.counter = 0

    def add_task(self, priority, description):
        """Add a task to the scheduler.

        Args:
            priority: An integer priority (lower = more urgent).
            description: A string describing the task.
        """
        # TODO: Push onto the heap with a tiebreaker
        heapq.heappush(self.heap, (priority, self.counter, description))
        self.counter += 1

    def next_task(self):
        """Remove and return the highest-priority task's description.

        Returns:
            The description string, or None if empty.
        """
        # TODO: Pop from the heap, return the description
        if not self.heap:
            return None
        return heapq.heappop(self.heap)[2]

    def peek(self):
        """Return the highest-priority task's description without removing it.

        Returns:
            The description string, or None if empty.
        """
        # TODO: Look at h[0] without popping
        if not self.heap:
            return None
        return self.heap[0][2]

    def __len__(self):
        """Return the number of pending tasks."""
        # TODO: Return the length of the heap
        return len(self.heap)

    def is_empty(self):
        """Return True if there are no pending tasks."""
        # TODO
        return not self.heap