# Lab 12: Breaking the O(n^2) Barrier

## Overview

In Lab 11, you discovered that two O(n^2) algorithms can behave very differently in practice — insertion sort's shifts are cheaper than bubble sort's swaps, and early termination can turn O(n^2) into O(n) on sorted input. But both algorithms share a fundamental limitation: they move items one position at a time.

What if we could move items *farther*? What if we could split the problem in half, sort each half, and combine the results? That's the leap from O(n^2) to O(n log n) — and it changes everything.

In this lab, you'll work with three algorithms that break the quadratic barrier. The recursive scaffolding is provided — your job is to implement the **core mechanism** of each:

- **Shell sort** — fill in the gap insertion sort (your Lab 11 insertion sort, adapted)
- **Merge sort** — fill in the merge step (combining two sorted halves)
- **Quicksort** — fill in the partition (splitting by value)

Then you'll use the analysis notebook to see the O(n^2) vs O(n log n) curves diverge — and discover quicksort's weakness.

**Starter files:** `sorting.py`, `test_sorting.py`, `analysis.ipynb`
**Test command:** `pytest -v` (from your Lab12 root)

## Part 1: Project Setup

Organize the starter files into the same structure you've been using:

```
Lab12/
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
5. Keep `conftest.py` in the Lab12 root
6. Verify: run `pytest -v` — all tests should **fail** (nothing is implemented yet)

**Commit checkpoint:**
```bash
git add -A
git commit -m "Lab 12: Organize project structure"
```

## Background: Beyond One Step at a Time

Every sorting algorithm you've written so far moves items **one position per comparison**. If an item is 50 positions away from where it belongs, it takes at least 50 operations to get there.

Shell sort asks: what if we sorted items that are *far apart* first? Merge sort and quicksort ask an even bigger question: what if we split the problem in half at every level?

### The Divide and Conquer Paradigm

If you split a list of n items in half:
- You get **log n levels** of splitting (you can only halve something log n times before reaching single items)
- Each level does **O(n) work** (touching every item once to split or merge)
- Total: **O(n log n)**

For n = 1,000: roughly 10,000 operations instead of 1,000,000. For n = 1,000,000: 20,000,000 instead of 1,000,000,000,000. The gap between n^2 and n log n isn't a small improvement — it's the difference between "finishes instantly" and "finishes never."

## Part 2: Implementation

Open `src/sorting.py`. You'll find three sections marked with TODO. The surrounding structure (recursive calls, entry points, counted versions) is already provided — focus on the core logic.

### Task 1: `_gap_insertion_sort(a_list, start, gap)` — Shell Sort's Engine

This is your insertion sort from Lab 11, adapted to work on items that are `gap` positions apart instead of adjacent. The outer `shell_sort` function (provided) calls this helper repeatedly with decreasing gaps.

**The adaptation is mechanical:** everywhere Lab 11's insertion sort used `1`, you use `gap`:
- Loop from `start + gap` to `len(a_list)`, stepping by `gap`
- Save `a_list[i]` as `current_value`, set `position = i`
- Walk backward by `gap`: while `position >= gap` and `a_list[position - gap] > current_value`, shift right by `gap`
- Place `current_value` at the insertion point

**Example with gap = 4 on positions {0, 4, 8} = {54, 77, 20}:**
```
Start with sublist [54, 77, 20]:
  i=4: 77 > 54? No shift needed. [54, 77, 20]
  i=8: 20 < 77? Shift 77 right. 20 < 54? Shift 54 right. Place 20. [20, 54, 77]
```

```bash
pytest -v -k "TestShellSort"
git add -A && git commit -m "Lab 12: Implement gap insertion sort for shell sort"
```

### Task 2: Merge Step in `merge_sort(a_list)` — Combining Sorted Halves

The recursive splitting and the function structure are provided. You fill in the **merge step** — the part that combines two sorted halves (`left` and `right`) back into `a_list`.

**The merge uses three index variables**, all starting at 0:
- `i` walks through `left`
- `j` walks through `right`
- `k` fills positions in `a_list`

**Three while loops:**

1. **Main merge** — while both halves have items (`i < len(left)` and `j < len(right)`):
   - Compare `left[i]` and `right[j]`
   - Take the smaller one (use `<=` for stability): put it at `a_list[k]`
   - Advance the index you took from, and advance `k`

2. **Left remainder** — while `i < len(left)`: copy `left[i]` to `a_list[k]`, advance both

3. **Right remainder** — while `j < len(right)`: copy `right[j]` to `a_list[k]`, advance both

**Example — merging [17, 54] and [26, 93]:**
```
Compare 17 vs 26 → take 17 from left,  a_list[0] = 17
Compare 54 vs 26 → take 26 from right, a_list[1] = 26
Compare 54 vs 93 → take 54 from left,  a_list[2] = 54
Left exhausted   → take 93 from right, a_list[3] = 93
Result: [17, 26, 54, 93]
```

```bash
pytest -v -k "TestMergeSort"
git add -A && git commit -m "Lab 12: Implement merge step for merge sort"
```

### Task 3: `_partition(a_list, first, last)` — Quicksort's Splitter

The recursive quicksort structure and entry point are provided. You fill in the **partition** — the function that picks a pivot and rearranges items so smaller values go left, larger values go right, and the pivot lands in its final position.

**The algorithm:**
1. `pivot_value = a_list[first]` (use the first item as pivot)
2. `left_mark = first + 1`, `right_mark = last`
3. Loop with a `done` flag until the markers cross:
   - Advance `left_mark` right while `left_mark <= right_mark` AND `a_list[left_mark] <= pivot_value`
   - Advance `right_mark` left while `left_mark <= right_mark` AND `a_list[right_mark] >= pivot_value`
   - If `right_mark < left_mark`: marks crossed, set `done = True`
   - Otherwise: swap `a_list[left_mark]` and `a_list[right_mark]`
4. Swap `a_list[first]` with `a_list[right_mark]` (pivot goes to final position)
5. Return `right_mark`

**Example — partitioning [54, 26, 93, 17, 77, 31, 44, 55, 20] with pivot 54:**
```
left_mark finds 93 (> 54 at index 2)
right_mark finds 20 (< 54 at index 8)
Swap 93 and 20 → [54, 26, 20, 17, 77, 31, 44, 55, 93]

left_mark finds 77 (> 54 at index 4)
right_mark finds 44 (< 54 at index 6)
Swap 77 and 44 → [54, 26, 20, 17, 44, 31, 77, 55, 93]

left_mark advances past right_mark → done
Swap pivot with right_mark → 54 lands in its final position
```

```bash
pytest -v -k "TestQuickSort"
git add -A && git commit -m "Lab 12: Implement partition for quicksort"
```

## Part 3: Analysis Notebook

This is where the numbers tell the real story. The notebook uses the **counted versions** (provided complete in your starter file) to measure comparisons and data moves across all algorithms.

### Opening the Notebook in Colab

Push your repo to GitHub first, then open it in Colab:

```
https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/labs/Lab12/notebooks/analysis.ipynb
```

1. Click **File > Save a copy in Drive**
2. Paste your completed sort functions into the first code cell
3. Run each experiment cell, then answer the questions in the markdown cells

### Experiment 1: Watching the Mechanism

Visual traces of all three algorithms on `[54, 26, 93, 17, 77, 31, 44, 55, 20]`.

**Questions to answer:**
- In shell sort, what happens to the list between the first gap pass and the last? Is it fully sorted before gap = 1, or just "closer to sorted"?
- In merge sort, how many levels of splitting happen for 9 items? Does the merge step at each level touch every item?
- In quicksort, how many items are permanently placed after each partition call?

### Experiment 2: Breaking the Barrier

The big moment. Runs bubble sort, insertion sort (from Lab 11, provided in the notebook), and your three Lab 12 sorts on lists from n = 100 to n = 10,000.

**Questions to answer:**
- At what list size do the O(n^2) and O(n log n) curves visibly diverge?
- At n = 10,000, roughly how many times more comparisons does bubble sort make than merge sort?
- Where does shell sort fall — closer to O(n^2) or O(n log n)?

### Experiment 3: Quicksort's Achilles Heel

Runs merge sort and quicksort on sorted, reverse-sorted, and random input (n = 1,000).

**Questions to answer:**
- On random input, do merge sort and quicksort make a similar number of comparisons?
- What happens to quicksort's comparison count on already-sorted input? Why?
- Given this weakness, why would anyone choose quicksort over merge sort? (Hint: look at memory usage)

### Saving Back to GitHub

1. **File > Save a copy in GitHub**
2. Select your repo, set path to `labs/Lab12/notebooks/analysis.ipynb`
3. Click OK

```bash
git pull
git add -A && git commit -m "Lab 12: Complete analysis notebook"
```

## Key Concepts

| Concept | What it means |
|---------|--------------|
| **Shell sort** | Insertion sort with decreasing gaps; bridges O(n^2) and O(n log n) |
| **Divide and conquer** | Split the problem in half, solve each half, combine results |
| **Merge sort** | Split by position, merge sorted halves; O(n log n) always, O(n) extra space |
| **Quicksort** | Split by value (pivot + partition); O(n log n) average, O(n^2) worst, in-place |
| **Partition** | Rearrange so items < pivot go left, items > pivot go right; pivot lands in final position |
| **Stability** | Equal items keep their original relative order (merge sort: yes, quicksort: no) |
| **O(n log n) vs O(n^2)** | The gap grows dramatically with n — this is THE reason algorithm choice matters |

## Submission

Push your completed code and submit your repo URL.

Your commit history should look something like:
```
Lab 12: Organize project structure
Lab 12: Implement gap insertion sort for shell sort
Lab 12: Implement merge step for merge sort
Lab 12: Implement partition for quicksort
Lab 12: Complete analysis notebook
```

```bash
git push
```
