# Lab 11: Sorting — Why Big-O Isn't the Whole Story

## Overview

In Lab 10, you discovered that binary search is dramatically faster than sequential search — but it only works on sorted data. You ended with a question: when is the cost of sorting worth it?

Now you're paying that cost. In this lab, you'll implement two sorting algorithms that both run in O(n^2) time. Same Big-O. Same complexity class. But when you instrument them and measure what's actually happening, you'll discover they behave *very* differently in practice. By the end, you'll understand why Big-O is a category, not a verdict.

**Starter files:** `sorting.py`, `test_sorting.py`, `analysis.ipynb`
**Test command:** `pytest -v` (from your Lab11 root)

## Part 1: Project Setup

Organize the starter files into the same structure you used in Lab 10:

```
Lab11/
├── README.md
├── conftest.py
├── src/
│   └── sorting.py
├── tests/
│   └── test_sorting.py
└── notebooks/
    └── analysis.ipynb
```

**Steps:**
1. Create the `src/`, `tests/`, and `notebooks/` directories
2. Move `sorting.py` into `src/`
3. Move `test_sorting.py` into `tests/`
4. Move `analysis.ipynb` into `notebooks/`
5. Keep `conftest.py` in the Lab11 root
6. Verify: run `pytest -v` — all tests should **fail** (nothing is implemented yet)

**Commit checkpoint:**
```bash
git add -A
git commit -m "Lab 11: Organize project structure"
```

## Background: How Sorting Works

You sort things every day without thinking about it. Arranging cards in your hand, organizing files by date, lining up in height order — sorting is one of the most fundamental operations in computing because so many other algorithms (like binary search) depend on it.

But here's the thing: there are *many* ways to sort a list, and they're not all created equal. The two algorithms you'll implement both get the job done, but they take very different approaches. Understanding the difference teaches you something important about algorithm analysis.

### The Unit of Work: Comparisons and Exchanges

To measure how much work a sorting algorithm does, we count two things:

**Comparisons** — every time the algorithm asks "is this item bigger or smaller than that one?" That's the detective work: figuring out what's out of order.

**Exchanges** — every time the algorithm swaps two items to fix an ordering problem. Swapping isn't free. In most languages, exchanging two items requires a temporary variable and three assignments:

```python
temp = a_list[i]
a_list[i] = a_list[j]
a_list[j] = temp
```

Why can't you just write `a_list[i] = a_list[j]` followed by `a_list[j] = a_list[i]`? Try it mentally — the first assignment destroys the original value at position `i` before you can copy it to position `j`. The temporary variable saves it.

Python has a shortcut — `a_list[i], a_list[j] = a_list[j], a_list[i]` — but under the hood, the same three-step dance is happening.

These two costs — comparisons and data movement — are **separate levers**. Two algorithms can make the same number of comparisons but move data very differently. That's the key insight of this lab.

## Part 2: Implementation

Open `src/sorting.py`. You'll find three functions to complete, plus two counted versions.

### Task 1: `bubble_sort(a_list)` — The Brute Force Approach

Bubble sort is the most straightforward sorting idea: walk through the list, compare each pair of adjacent items, and swap any pair that's out of order. Repeat until the list is sorted.

**Here's how it works:**

On each pass, the algorithm walks from position 0 to the end of the unsorted region, comparing each item to the one next to it. If they're out of order, it swaps them. After one complete pass, the largest unsorted item has "bubbled up" to its correct position at the end.

```
Pass 1 through [54, 26, 93, 17, 77]:

  Compare 54, 26 → swap  → [26, 54, 93, 17, 77]
  Compare 54, 93 → ok    → [26, 54, 93, 17, 77]
  Compare 93, 17 → swap  → [26, 54, 17, 93, 77]
  Compare 93, 77 → swap  → [26, 54, 17, 77, 93]
                                             ✓ 93 is in place
```

After pass 1, the largest item (93) is in its final position. After pass 2, the second-largest is in place. And so on.

**The algorithm:**
1. Make `n - 1` passes through the list (where `n` is the length)
2. On each pass `i` (starting from 0), compare adjacent items from position 0 up to position `n - 1 - i` (because the last `i` items are already sorted)
3. If `a_list[j] > a_list[j + 1]`, swap them

**Important:** Your function should sort the list **in place** (modify the original list) and also **return it**.

**Hint:** This is a nested loop. The outer loop controls the number of passes. The inner loop walks through the unsorted portion. The inner loop's range shrinks by one each pass — think about why.

```bash
pytest -v -k "TestBubbleSort"
git add -A && git commit -m "Lab 11: Implement bubble sort"
```

### Task 2: `short_bubble_sort(a_list)` — Knowing When to Stop

Your bubble sort always makes `n - 1` passes, even if the list becomes sorted after pass 2. That's wasted work.

Here's the insight: if you make a complete pass through the list and **no swaps happen**, the list must already be sorted. Think about why — if no adjacent pair was out of order, then every item is less than or equal to the one after it. That's the definition of sorted.

**Your job:** Copy your bubble sort logic and add one thing — a boolean flag that tracks whether any exchange happened during each pass. If a pass completes with no exchanges, return immediately.

**The change is small but the impact is real:**
- Already-sorted list: standard bubble sort still makes `n - 1` passes. Short bubble? **One pass.** It checks every adjacent pair, sees nothing to swap, and stops.
- Nearly-sorted list (a few items out of place): short bubble finishes in just a few passes instead of grinding through all of them.

**Hint:** Set a flag to `False` at the start of each pass. Set it to `True` whenever you make a swap. After the pass, check the flag.

```bash
pytest -v -k "TestShortBubbleSort"
git add -A && git commit -m "Lab 11: Implement short bubble sort"
```

### Task 3: `insertion_sort(a_list)` — A Different Philosophy

Bubble sort works from the end of the list backward, placing the largest unsorted item in its final position each pass. Insertion sort takes the opposite approach: it works from the **front**, building a sorted region that grows one item at a time.

**The idea:** Imagine you're holding a hand of cards. You pick up cards one at a time. Each time you pick up a new card, you slide it into the correct position among the cards you're already holding. After picking up all the cards, your hand is sorted.

```
Sorting [54, 26, 93, 17, 77]:

Start: sorted region = [54]  |  unsorted = [26, 93, 17, 77]

Pass 1: insert 26 into [54]
  26 < 54 → shift 54 right → insert 26
  [26, 54]  |  [93, 17, 77]

Pass 2: insert 93 into [26, 54]
  93 > 54 → already in place
  [26, 54, 93]  |  [17, 77]

Pass 3: insert 17 into [26, 54, 93]
  17 < 93 → shift 93 right
  17 < 54 → shift 54 right
  17 < 26 → shift 26 right → insert 17
  [17, 26, 54, 93]  |  [77]

Pass 4: insert 77 into [17, 26, 54, 93]
  77 < 93 → shift 93 right
  77 > 54 → insert 77
  [17, 26, 54, 77, 93]  ✓ done
```

Notice something important: insertion sort doesn't swap. It **shifts**. When an item needs to move, existing items slide over one position to make room. A shift is a single assignment — not the three assignments of a full swap. That makes insertion sort roughly **three times cheaper** on data movement than bubble sort, even when both make the same number of comparisons.

**The algorithm:**
1. Start at position 1 (position 0 is already "sorted" by itself)
2. For each position `i`, save the current item in a variable (`current_value`)
3. Walk backward through the sorted region (positions `i-1` down to 0):
   - If the item at position `j` is greater than `current_value`, shift it right (copy it to position `j + 1`)
   - If the item at position `j` is less than or equal to `current_value`, stop — you've found the insertion point
4. Place `current_value` at the insertion point

**The tricky part:** Getting the backward walk right. You need a `while` loop (not a `for` loop) because you're checking two conditions: you haven't gone past the start of the list AND the current item is still smaller than what's there. Think about the order of those checks — what happens if `position` reaches -1?

**Hint:** Use a variable called `position` that starts at `i - 1` and decrements. Your while condition should check `position >= 0` first (why first?) and then check whether the item at `position` is greater than `current_value`.

```bash
pytest -v -k "TestInsertionSort"
git add -A && git commit -m "Lab 11: Implement insertion sort"
```

### Task 4: `bubble_sort_counted(a_list)` and `insertion_sort_counted(a_list)` — Counting the Work

Now the interesting part. Create counted versions of bubble sort and insertion sort that track **both** comparisons and data movement separately.

Return a tuple: `(sorted_list, comparisons, data_moves)` where:
- `comparisons` = how many times you compared two items
- `data_moves` = how many exchanges (for bubble sort) or shifts + final insertion (for insertion sort)

**Counting rules for bubble sort:**
- Each `if a_list[j] > a_list[j+1]` check is **one comparison**
- Each swap is **one exchange** (count the whole swap as one data move, not three assignments)

**Counting rules for insertion sort:**
- Each time you check whether `a_list[position] > current_value` is **one comparison**
- Each shift (moving an item one position right) is **one data move**
- The final placement of `current_value` into its position is **one data move**

**Example:**
```python
bubble_sort_counted([3, 1, 2])
# → ([1, 2, 3], 3, 2)
#    Pass 1: compare(3,1)→swap, compare(3,2)→swap → 2 comparisons, 2 exchanges
#    Pass 2: compare(1,2)→ok → 1 comparison, 0 exchanges
#    Total: 3 comparisons, 2 exchanges

insertion_sort_counted([3, 1, 2])
# → ([1, 2, 3], 3, 4)
#    Pass 1: insert 1 → compare with 3 (>1, shift) → stop → place 1. 1 comparison, 2 data moves (1 shift + 1 placement)
#    Pass 2: insert 2 → compare with 3 (>2, shift) → compare with 1 (not >2, stop) → place 2. 2 comparisons, 2 data moves (1 shift + 1 placement)
#    Total: 3 comparisons, 4 data moves
```

Wait — insertion sort has *more* data moves in that example? Don't worry. The counted versions aren't about which number is bigger — they're about measuring two different *kinds* of cost. You'll see what this means in the notebook.

```bash
pytest -v -k "TestCounted"
git add -A && git commit -m "Lab 11: Add comparison and data-move counting"
```

## Part 3: Analysis Notebook

This is where the numbers tell a story your code alone doesn't.

### Opening the Notebook in Colab

Push your repo to GitHub first, then open it in Colab:

```
https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/labs/Lab11/notebooks/analysis.ipynb
```

1. Click **File > Save a copy in Drive** — this gives you an editable copy
2. Paste your completed sort functions (all five — three originals plus two counted versions) into the first code cell
3. Run each experiment cell, then answer the questions in the markdown cells below it

### Experiment 1: Watching the Mechanism

Before we measure anything, let's *see* how these algorithms work. The notebook includes a helper function that prints the list state after each pass for both bubble sort and insertion sort.

Run it on the list `[54, 26, 93, 17, 77, 31, 44, 55, 20]` and study the output.

**Questions to answer:**
- In bubble sort, where do the sorted items accumulate? (Which end of the list?) In insertion sort, where do they accumulate?
- Watch bubble sort's first few passes. How much does the unsorted region change after each pass? Now watch insertion sort. How much does the sorted region change after each pass?
- Which algorithm's progress is easier to follow visually? Why do you think that is?

### Experiment 2: The Comparison Race

Run both counted sort functions on randomly generated lists of increasing size: n = 100, 500, 1,000, and 5,000. For each size, record comparisons and data moves. Plot them.

The notebook gives you two graphs: one for comparisons, one for data moves.

**Questions to answer:**
- Look at the comparisons graph. Do bubble sort and insertion sort make roughly the same number of comparisons, or is one consistently higher? Does this match what you'd expect from their shared O(n^2) classification?
- Now look at the data moves graph. What do you see? Which algorithm moves data more efficiently?
- If comparisons are roughly equal but data movement is very different, what does that tell you about using Big-O alone to predict real-world performance?

### Experiment 3: Best Case, Worst Case

Not all inputs are created equal. Run both counted sort functions on three kinds of input (n = 1,000):
- **Already sorted:** `list(range(1000))`
- **Reverse sorted:** `list(range(999, -1, -1))`
- **Random:** a shuffled list

Record comparisons and data moves for each case.

**Questions to answer:**
- Which sort benefits the most from already-sorted input? Look at both comparisons and data moves — does either drop dramatically?
- On reverse-sorted input, which sort performs worst? Why does that specific input cause the most work?
- If you knew your data was *almost* sorted (say, one or two items out of place), which algorithm would you choose? Why? Think about your short bubble implementation — how would it perform here?

### Saving Back to GitHub

1. **File > Save a copy in GitHub**
2. Select your repo, set path to `labs/Lab11/notebooks/analysis.ipynb`
3. Click OK

```bash
git pull
git add -A && git commit -m "Lab 11: Complete analysis notebook"
```

## Key Concepts

| Concept | What it means |
|---------|--------------|
| **Bubble sort** | Repeatedly walk the list, swapping adjacent out-of-order pairs; O(n^2) |
| **Short bubble sort** | Bubble sort with early termination when no swaps occur; O(n) best case |
| **Insertion sort** | Build a sorted region from the left, inserting each new item in its place; O(n^2) worst, O(n) best |
| **Comparisons** | How many times the algorithm asks "which is bigger?" |
| **Exchanges vs shifts** | A swap costs 3 assignments; a shift costs 1 — same effect, different price |
| **Big-O is a category** | Two O(n^2) algorithms can have very different real-world performance |

## Submission

Push your completed code and submit your repo URL.

Your commit history should look something like:
```
Lab 11: Organize project structure
Lab 11: Implement bubble sort
Lab 11: Implement short bubble sort
Lab 11: Implement insertion sort
Lab 11: Add comparison and data-move counting
Lab 11: Complete analysis notebook
```

```bash
git push
```
