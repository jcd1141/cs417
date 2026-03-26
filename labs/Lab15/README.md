# Lab 15: Priority in Practice — Heaps and `heapq`

## Overview

In Lab 14, you implemented tree traversals by hand — recursion, base cases, building results node by node. You saw the tree, understood its shape, and wrote the code that walked it.

Now you're going to use a tree-based structure without ever seeing the tree. Python's `heapq` module gives you a **heap** — a complete binary tree that keeps the smallest value at the top — but it hides the tree behind a plain list and a few function calls. You push things in, you pop things out, and the highest-priority item always comes out first. The bubble-up and sink-down operations you learned in lecture? `heapq` does them for you.

Your job in this lab is to go from understanding the API to **building something with it**: a task scheduler that manages priorities, handles ties fairly, and processes a dynamic workload.

**Starter files:** `heap_basics.py`, `scheduler.py`, `test_heap.py`, `conftest.py`
**Test command:** `pytest -v` (from your Lab15 root)

## Part 1: Project Setup

```
Lab15/
├── README.md
├── conftest.py
├── src/
│   ├── heap_basics.py
│   └── scheduler.py
└── tests/
    └── test_heap.py
```

1. Create the `src/` and `tests/` directories
2. Move files into their places
3. Verify: `pytest -v` — all tests should **fail**

```bash
git add -A && git commit -m "Lab 15: Organize project structure"
```

## Background: From Tree to Tool

Remember the three-layer model from lecture:

- **Priority queue** = the abstract idea. Insert items with priorities, always get the most important one next.
- **Heap** = the data structure. A complete binary tree where every parent beats its children.
- **`heapq`** = the Python library. It does the heap operations on a regular list.

You don't create a special heap object. You just use a regular Python list and call `heapq` functions on it:

```python
import heapq

h = []                      # a regular list — heapq treats it as a heap
heapq.heappush(h, 5)        # insert 5
heapq.heappush(h, 2)        # insert 2
heapq.heappush(h, 8)        # insert 8

print(h[0])                 # peek at the smallest → 2
smallest = heapq.heappop(h) # remove and return the smallest → 2
```

Three things to remember:
- **`heapq` is a min-heap.** The smallest value is always at the top. Lower number = higher priority.
- **`h[0]` is peek.** It gives you the minimum without removing it.
- **`heapq.heapify(existing_list)`** turns any list into a valid heap in-place.

That's the entire API you need for this lab.

## Part 2: Heap Basics

### Task 1: Explore `heapq`

Open `src/heap_basics.py`. You'll find three functions to implement. Each one is a small exercise with `heapq` — nothing fancy, just getting your fingers used to the API.

**`push_and_pop(values)`** — Take a list of numbers, push each one onto a heap, then pop them all off and return them as a list. The returned list should be in ascending order (smallest first) — not because you sorted it, but because that's what the heap gives you.

**`heapify_and_peek(values)`** — Take a list of numbers, turn it into a heap using `heapq.heapify()`, and return the smallest value without removing it.

**`top_k_smallest(values, k)`** — Given a list of numbers and an integer `k`, return the `k` smallest values in ascending order. There's more than one way to do this with `heapq` — pick whichever feels natural.

**Hint:** For `top_k_smallest`, you could push everything and pop `k` times. Or check what `heapq.nsmallest()` does.

```bash
pytest -v -k "TestHeapBasics"
git add -A && git commit -m "Lab 15: Explore heapq basics"
```

## Background: Tuples and Priorities

Real-world priority queues don't just hold numbers — they hold *items* with priorities. In `heapq`, you do this with **tuples**:

```python
import heapq

h = []
heapq.heappush(h, (2, "fix login bug"))
heapq.heappush(h, (1, "server is down"))
heapq.heappush(h, (3, "update docs"))

task = heapq.heappop(h)  # → (1, "server is down")
```

The heap compares tuples element by element — so the first element (the priority number) controls the order. Lower number = higher priority.

**But there's a catch.** What happens when two tasks have the same priority?

```python
heapq.heappush(h, (1, "server down"))
heapq.heappush(h, (1, "database down"))  # same priority!
```

Python tries to compare the second element to break the tie. If the second elements are strings, that works (alphabetical order) — but it's not what you want. You want **FIFO**: if two tasks have the same priority, the one that arrived first should come out first.

The fix: add a **sequence counter** as a tiebreaker:

```python
heapq.heappush(h, (1, 0, "server down"))    # priority 1, arrived 0th
heapq.heappush(h, (1, 1, "database down"))   # priority 1, arrived 1st
```

Now ties are broken by arrival order, and Python never needs to compare the strings.

## Part 3: Tuple Priorities

### Task 2: Priority Sorting with Tuples

In `src/heap_basics.py`, implement:

**`sort_by_priority(tasks)`** — Takes a list of `(priority, description)` tuples. Return the descriptions (just the strings) in priority order (lowest priority number first). For tasks with the same priority, maintain their original order (FIFO).

You'll need to use the tiebreaker pattern from the background section. Push each task onto a heap with a sequence counter, then pop them all off.

**Example:**
```python
tasks = [(3, "update docs"), (1, "server down"), (1, "database down"), (2, "fix bug")]
sort_by_priority(tasks)
# → ["server down", "database down", "fix bug", "update docs"]
```

Notice "server down" comes before "database down" — same priority, but "server down" was listed first.

```bash
pytest -v -k "TestTuplePriorities"
git add -A && git commit -m "Lab 15: Tuple priorities with tiebreaker"
```

## Part 4: Build a Task Scheduler

### Task 3: `TaskScheduler`

Now put it all together. Open `src/scheduler.py`. You'll build a `TaskScheduler` class that manages a priority queue of tasks.

The scheduler needs three things:

**`add_task(priority, description)`** — Add a task to the scheduler. Lower priority number = more urgent. Tasks with the same priority should be processed in the order they were added (FIFO).

**`next_task()`** — Remove and return the description of the highest-priority task. If the scheduler is empty, return `None`.

**`peek()`** — Return the description of the highest-priority task *without* removing it. If the scheduler is empty, return `None`.

You'll also need:

**`__len__()`** — Return the number of pending tasks. This lets `len(scheduler)` work.

**`is_empty()`** — Return `True` if there are no pending tasks.

Here's how it should work:

```python
s = TaskScheduler()
s.add_task(2, "fix login bug")
s.add_task(1, "server is down")
s.add_task(3, "update docs")

s.peek()       # → "server is down" (priority 1, most urgent)
s.next_task()   # → "server is down" (removed)
s.next_task()   # → "fix login bug" (priority 2 is next)
len(s)          # → 1
s.next_task()   # → "update docs"
s.next_task()   # → None (empty)
```

**Think about:**
- What's your internal data structure? (A list that `heapq` manages.)
- How do you handle the tiebreaker? (You solved this in Task 2.)
- What does each tuple on the heap look like?

```bash
pytest -v -k "TestTaskScheduler"
git add -A && git commit -m "Lab 15: Implement TaskScheduler"
```

## Key Concepts

| Concept | What it means |
|---------|--------------|
| **Priority queue** | An abstract data type: insert with a priority, always retrieve the highest-priority item next |
| **Heap** | A complete binary tree where every parent beats its children — the implementation behind priority queues |
| **`heapq`** | Python's heap library — operates on a regular list, gives you O(log n) insert and extract |
| **Min-heap** | The smallest value is always at the top — `heapq`'s default behavior |
| **Tuple comparison** | Python compares tuples element by element — first element controls heap ordering |
| **Sequence counter** | A tiebreaker in heap tuples — ensures FIFO order when priorities are equal |
| **`h[0]`** | Peek at the minimum without removing it — O(1) |
| **`heapify()`** | Convert an existing list into a valid heap in-place — O(n) |

## Submission

Push your completed code and submit your repo URL.

Your commit history should look something like:
```
Lab 15: Organize project structure
Lab 15: Explore heapq basics
Lab 15: Tuple priorities with tiebreaker
Lab 15: Implement TaskScheduler
```

```bash
git push
```