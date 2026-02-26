# Lab 10: Searching — From Linear Scan to Divide and Conquer

## Overview

In Labs 8 and 9, you built hash tables — data structures that look up values in O(1) time. That's incredibly fast, but hash tables don't preserve order. You can't ask a hash table "what's the smallest key?" or "give me everything between 10 and 20" without checking every slot.

What if your data is sorted? A sorted list gives you structure you can exploit — but *how* you search it matters enormously. In this lab, you'll implement two search algorithms and discover exactly when the smarter one becomes worth the effort.

**Starter files:** `search.py`, `test_search.py`, `analysis.ipynb`
**Test command:** `pytest -v` (from your Lab10 root)

## Part 1: Project Setup

Organize the starter files into a proper project structure:

```
Lab10/
├── README.md
├── conftest.py
├── src/
│   └── search.py
├── tests/
│   └── test_search.py
└── notebooks/
    └── analysis.ipynb
```

**Steps:**
1. Create the `src/`, `tests/`, and `notebooks/` directories
2. Move `search.py` into `src/`
3. Move `test_search.py` into `tests/`
4. Move `analysis.ipynb` into `notebooks/`
5. Keep `conftest.py` in the Lab10 root
6. Verify: run `pytest -v` — all tests should **fail** (nothing is implemented yet)

**Commit checkpoint:**
```bash
git add -A
git commit -m "Lab 10: Organize project structure"
```

## Background: How Search Works

You use search every day. Looking up a contact on your phone, finding a word in a document, checking if a username is taken — all of these are search problems. The question is: how many items do you have to look at before you find what you want (or confirm it's not there)?

### The Brute Force Approach

The simplest strategy: start at the beginning, check every item, stop when you find it or reach the end. This is **sequential search** (also called linear search).

```
Search for 17 in [4, 8, 2, 15, 17, 23, 42, 11]:

  [4]  → not 17
  [8]  → not 17
  [2]  → not 17
  [15] → not 17
  [17] → found it! (5 comparisons)
```

What if the item isn't there?

```
Search for 99 in [4, 8, 2, 15, 17, 23, 42, 11]:

  [4]  → not 99
  [8]  → not 99
  [2]  → not 99
  [15] → not 99
  [17] → not 99
  [23] → not 99
  [42] → not 99
  [11] → not 99
  → Not found. (8 comparisons — checked every single item)
```

In the worst case, you check every item. That's O(n) — the time grows directly with the size of the list. For 10 items, that's fine. For 10 million? That's a problem.

### Exploiting Sorted Order

Now imagine the list is sorted. Can you do better than checking every item?

```
Search for 17 in [2, 4, 8, 11, 15, 17, 23, 42]:

  Start at the middle → 11. Is 17 bigger or smaller?
  Bigger. So 17 can't be in the left half. Eliminate [2, 4, 8, 11].

  Middle of what's left → 23. Is 17 bigger or smaller?
  Smaller. Eliminate [23, 42].

  Middle of what's left → 15. Bigger.
  Next → 17. Found it! (4 comparisons)
```

Each comparison eliminates **half** the remaining items. After 1 comparison, n/2 remain. After 2, n/4. After 3, n/8. After *k* comparisons, n/2^k remain. When does that hit 1? When k = log₂(n).

That's **binary search** — O(log n). For a list of 10 million items, sequential search might need 10 million comparisons. Binary search needs at most **24**.

But there's a catch: binary search only works on sorted data. And sorting isn't free.

## Part 2: Implementation

Open `src/search.py`. You'll find two functions to complete.

### Task 1: `sequential_search(a_list, target)` — The Baseline

Implement sequential search. Walk through the list from position 0, compare each item to the target:
- If you find it → return `True`
- If you reach the end → return `False`

This should feel straightforward — that's intentional. It's the baseline you'll measure everything else against.

**Hint:** A simple `for` loop over the list.

```bash
pytest -v -k "TestSequentialSearch"
git add -A && git commit -m "Lab 10: Implement sequential search"
```

### Task 2: `binary_search(a_list, target)` — The Divide and Conquer

Implement binary search on a **sorted** list. This is where you need to think carefully.

**Here's the algorithm:**
1. Track two boundaries: `first` (initially 0) and `last` (initially `len(a_list) - 1`)
2. While `first <= last`:
   - Compute the midpoint: `mid = (first + last) // 2`
   - If `a_list[mid] == target` → return `True`
   - If `target < a_list[mid]` → the target is in the left half → update `last = mid - 1`
   - If `target > a_list[mid]` → the target is in the right half → update `first = mid + 1`
3. If the loop ends without finding the target → return `False`

**The tricky part:** Getting the boundary updates right. Off-by-one errors are the most common binary search bug — it's famously difficult to write a correct binary search on the first try. The tests will catch these bugs, so use them.

**Trace through an example before you code.** Try searching for 6 in `[1, 3, 5, 7, 9, 11]`:
- first=0, last=5, mid=2 → a_list[2]=5 → 6 > 5 → first=3
- first=3, last=5, mid=4 → a_list[4]=9 → 6 < 9 → last=3
- first=3, last=3, mid=3 → a_list[3]=7 → 6 < 7 → last=2
- first=3, last=2 → first > last → return False

**Hint for the loop:** `while first <= last` — the `=` matters. If `first == last`, there's still one element to check.

```bash
pytest -v -k "TestBinarySearch"
git add -A && git commit -m "Lab 10: Implement binary search"
```

### Task 3: `sequential_search_counted(a_list, target)` and `binary_search_counted(a_list, target)` — Counting the Work

Now the interesting part. Go back to your two search functions and create counted versions. These work exactly like the originals, but they also **count the number of comparisons** made during the search and return both results.

Return a tuple: `(found, comparisons)` where `found` is `True`/`False` and `comparisons` is the number of times you compared an element to the target.

**Example:**
```python
sequential_search_counted([4, 8, 2, 15, 17], 17)  # → (True, 5)
sequential_search_counted([4, 8, 2, 15, 17], 99)  # → (False, 5)
binary_search_counted([2, 4, 8, 15, 17], 17)       # → (True, 3)
binary_search_counted([2, 4, 8, 15, 17], 99)       # → (False, 3)
```

Think about where comparisons happen in each algorithm. In sequential search, it's every time you check `a_list[i] == target`. In binary search, it's every time you check `a_list[mid]` against the target.

```bash
pytest -v -k "TestCounted"
git add -A && git commit -m "Lab 10: Add comparison counting"
```

## Part 3: Analysis Notebook

This is where you discover something the code alone doesn't show you.

### Opening the Notebook in Colab

The starter notebook (`analysis.ipynb`) is already in your repo — you moved it to `notebooks/` in Part 1. Push your repo to GitHub first, then open it in Colab:

```
https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/labs/Lab10/notebooks/analysis.ipynb
```

### Working in Colab

1. Click **File > Save a copy in Drive** — this gives you an editable copy
2. Paste your completed search functions (all four — original and counted versions) into the first code cell
3. Run each experiment cell, then answer the questions in the markdown cells below it

### What You'll Explore

Each experiment has two parts: **run the code** and **write up what you found**. Your writeup doesn't need to be long — a few sentences per question is fine — but it should show that you're thinking about *why* the results look the way they do, not just reporting numbers.

**Experiment 1: The Comparison Race**

Run both counted searches on randomly generated sorted lists of increasing size (n = 10, 100, 1,000, 10,000). For each size, search for a random target and record the comparison counts. Plot both on the same graph.

**Questions to answer:**
- Describe the shape of each curve. Why does one grow so much faster than the other?
- At what list size does the difference start to feel significant?

**Experiment 2: Best Case, Worst Case**

For sequential search, what's the best case? (Target is the first element.) What's the worst case? (Target isn't in the list.) Run both on a list of 10,000 items and compare.

For binary search, does it matter where the target is in the list? Run it on the first element, the last element, an element in the middle, and an element that's not there. How much do the comparison counts vary?

**Questions to answer:**
- Why does sequential search have such a huge gap between best and worst case?
- Why is binary search so consistent regardless of where the target is? What about the algorithm causes this?

**Experiment 3: When Is Sorting Worth It?**

Here's the real question. Binary search is faster — but it requires sorted data. Sorting isn't free.

Python's built-in `sorted()` function is O(n log n). Suppose you have an unsorted list of n items, and you need to search it *k* times. You have two options:

- **Option A:** Just use sequential search each time. Total cost: k × n comparisons.
- **Option B:** Sort the list first (cost: n log n), then use binary search for each search. Total cost: n log n + k × log n.

For n = 10,000: how many searches *k* do you need before Option B becomes cheaper? Calculate it, then verify experimentally.

**Questions to answer:**
- Show your math for the crossover point. At what value of *k* does Option B become cheaper?
- Does your experimental result match your calculation? If not, why might they differ?
- Give a real-world example where you'd choose Option A and one where you'd choose Option B.

### Saving Back to GitHub

1. **File > Save a copy in GitHub**
2. Select your repo, set path to `labs/Lab10/notebooks/analysis.ipynb`
3. Click OK

```bash
git pull
git add -A && git commit -m "Lab 10: Complete analysis notebook"
```

## Key Concepts

| Concept | What it means |
|---------|--------------|
| **Sequential search** | Check every item from the start; O(n) |
| **Binary search** | Halve the search space each step; O(log n); requires sorted data |
| **Comparisons** | The unit of work — how many times you check an element against the target |
| **Best/worst/average case** | Same algorithm, very different performance depending on input |
| **The sorting tradeoff** | Sorting costs O(n log n) upfront but unlocks O(log n) search — worth it only if you search enough times |
| **Divide and conquer** | Solve a problem by splitting it in half, solving each half, combining results |

## Submission

Push your completed code and submit your repo URL.

Your commit history should look something like:
```
Lab 10: Organize project structure
Lab 10: Implement sequential search
Lab 10: Implement binary search
Lab 10: Add comparison counting
Lab 10: Complete analysis notebook
```

```bash
git push
```
