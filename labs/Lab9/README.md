# Lab 9: Open Addressing with Linear Probing

## Overview

In Lab 8, you built a hash table that handled collisions with **separate chaining** — each bucket was a list that could hold multiple pairs. That works, but it means your hash table is really an array of linked lists.

What if each slot held **exactly one item**? No lists, no chains — just a flat array. That's **open addressing**. When a collision happens, you don't add to a list. You **probe** forward through the array until you find an empty slot.

This approach is how real hash tables in languages like Python and Rust actually work. Because all the data lives in one flat array (instead of scattered across separate lists), the computer can access it faster — it's all packed together in memory. But open addressing introduces a tricky problem when you try to delete something. You'll discover that problem and solve it in this lab.

**Time:** ~45 minutes
**Starter files:** `hash_table_open.py`, `test_hash_table.py`, `test_tombstones.py`, `conftest.py`
**Test command:** `pytest -v` (from your Lab9 root)

## Part 1: Project Setup

The starter files are flat — everything in one directory. Before writing any code, reorganize them into a proper project structure:

```
Lab9/
├── README.md
├── conftest.py            ← stays in root (pytest finds it here)
├── src/
│   └── hash_table_open.py
├── tests/
│   ├── test_hash_table.py
│   └── test_tombstones.py
└── notebooks/
    └── analysis.ipynb
```

**Steps:**
1. Create the `src/`, `tests/`, and `notebooks/` directories
2. Move `hash_table_open.py` into `src/`
3. Move both test files into `tests/`
4. Keep `conftest.py` in the Lab9 root (it tells pytest where to find your code)
5. Verify: run `pytest -v` from the Lab9 root — all tests should **fail** (that's correct, you haven't implemented anything yet)

**Commit checkpoint:**
```bash
git add -A
git commit -m "Lab 9: Organize project structure"
```

## Background: Open Addressing vs Chaining

In **chaining** (Lab 8), collisions share a bucket:
```
Bucket 0: []
Bucket 1: [("banana", 3), ("grape", 8)]    ← two items, one bucket
Bucket 2: []
```

In **open addressing**, every item gets its own slot. When a collision happens, you search forward for the next empty slot. This is called **linear probing**:

```
Insert "cat"→5:   hash("cat") = 2   → slot 2 is empty → place it there
Insert "dog"→3:   hash("dog") = 2   → slot 2 is taken → try 3 → empty → place it there
Insert "bird"→7:  hash("bird") = 2  → slot 2 taken → 3 taken → try 4 → empty → place it there

Table (size=7):
  [0] empty
  [1] empty
  [2] ("cat", 5)       ← cat hashes here
  [3] ("dog", 3)       ← dog probed 1 step
  [4] ("bird", 7)      ← bird probed 2 steps
  [5] empty
  [6] empty
```

### How Lookup Works

To **find** a key, you retrace the same probe path. Looking up `"bird"` in the table above:

```
get("bird"):  hash("bird") = 2
  slot 2 → ("cat", 5) — not "bird", keep probing
  slot 3 → ("dog", 3) — not "bird", keep probing
  slot 4 → ("bird", 7) — found it! return 7
```

What if we look up a key that isn't there?

```
get("fish"):  hash("fish") = 2
  slot 2 → ("cat", 5) — not "fish", keep probing
  slot 3 → ("dog", 3) — not "fish", keep probing
  slot 4 → ("bird", 7) — not "fish", keep probing
  slot 5 → empty — STOP. If "fish" were in the table, it would have been
                    placed here or earlier. An empty slot means "nothing was
                    ever pushed to this slot by a collision," so we can
                    safely say: KeyError, "fish" is not in the table.
```

This is the key insight: **empty slots act as stop signals**. The search knows it can quit because nothing could exist beyond an empty slot in the probe chain. Remember this — it becomes very important when we get to deletion.

### Key Difference from Lab 8

The load factor can never exceed 1.0. Why? With chaining, each bucket is a list that can grow forever — you just keep appending. With open addressing, each slot holds exactly one item. Once every slot is taken, there's physically no room. Your `put` should raise an `Exception` if the table is full.

## Part 2: Implementation

Open `src/hash_table_open.py` and complete the four `TODO` methods. Each slot in `self.table` is one of:
- `None` — empty (never used)
- `_TOMBSTONE` — deleted (we'll get to this in Task 4)
- `(key, value)` — a tuple holding a key-value pair

You'll see `_TOMBSTONE = object()` at the top of the file. This creates a unique marker value — it's not `None`, it's not a tuple, it's just a special flag we can check for. Think of it like a "reserved" sign on a restaurant table.

### Task 1: `_hash(self, key)` — The Hash Function

Same as Lab 8 — use Python's `hash()` and modulo to get a valid index.

**Hint:** One line, identical to Lab 8.

```bash
pytest -v -k "TestHashFunction"
git add -A && git commit -m "Lab 9: Implement _hash"
```

### Task 2: `put(self, key, value)` — Insert with Linear Probing

This is where open addressing gets interesting. You can't just append to a list — you need to **probe** for an open slot.

**Here's the algorithm:**
1. Compute the starting index with `_hash(key)`
2. Walk forward through the table (wrapping around with `%`), checking each slot:
   - If the slot is `None` → place `(key, value)` here, increment count, done
   - If the slot has a tuple with the **same key** → update the value (don't increment count), done
   - Otherwise → keep probing (move to the next index)
3. If you've checked every slot and found no room → raise `Exception("Hash table is full")`

> **Note:** After you complete Task 4, you'll come back and add one more condition to step 2 — treating `_TOMBSTONE` slots as open for insertion. For now, just handle `None` and existing keys.

**Example — inserting with a collision:**
```python
ht = HashTableOpen(size=5)
ht.put("apple", 1)    # hash → 3, slot 3 is empty → place it
ht.put("banana", 2)   # hash → 3, slot 3 is taken → try 4 → empty → place it
ht.put("banana", 99)  # hash → 3, slot 3 is "apple" → try 4 → "banana"! → update to 99
```

**Hint for wrapping:** `index = (start + step) % self.size` lets you loop around from the end of the table back to the beginning.

**Hint for the loop:** Use `for step in range(self.size):` to try every slot exactly once.

```bash
pytest -v -k "TestPut"
git add -A && git commit -m "Lab 9: Implement put with linear probing"
```

### Task 3: `get(self, key)` — Look Up with Probing

Finding a key follows the same probe path as inserting it (see "How Lookup Works" in the Background section):

1. Start at `_hash(key)`
2. Walk forward:
   - If the slot has a tuple with the **matching key** → return the value
   - If the slot is `None` → the key isn't in the table → raise `KeyError`
   - If the slot has a different key → keep probing
3. If you've checked every slot → raise `KeyError`

Remember from the Background section: `None` means "nothing was ever placed here," so you can safely stop searching. This is just the same logic from `put`, but returning a value instead of placing one.

> **Note:** After you complete Task 4, you'll come back and add handling for `_TOMBSTONE` — when you encounter one, skip over it and keep probing. You'll understand why once you see the tombstone problem.

```bash
pytest -v -k "TestGet"
git add -A && git commit -m "Lab 9: Implement get with probe search"
```

### Task 4: `delete(self, key)` — The Tombstone Problem

Here's the tricky part. Think back to the Background section: `get` stops searching when it hits an empty slot (`None`), because `None` means "nothing was ever placed here." That assumption is what makes lookup fast — you don't have to check the entire table.

But what happens if we delete a key by setting its slot back to `None`?

```
Before delete — all three keys hash to index 2:
  [2] ("cat", 5)
  [3] ("dog", 3)       ← we want to delete this
  [4] ("bird", 7)

WRONG — set slot 3 to None:
  [2] ("cat", 5)
  [3] None              ← gap!
  [4] ("bird", 7)

Now try to find "bird":
  hash("bird") → 2 → found "cat", not a match
  probe → 3 → None → STOP. "Nothing was ever placed here."
  KeyError: "bird"

But "bird" IS in the table at slot 4! The empty gap sent a false signal —
it told get() that no collision ever pushed a key past this point,
which is a lie. The probe chain is broken.
```

**The fix: tombstones.** Instead of setting the slot to `None`, set it to `_TOMBSTONE`. The name comes from a gravestone — it marks where something used to live but is now gone. A tombstone tells `get()`: "something WAS here, so keys might have been pushed past me. Keep looking."

```
RIGHT — set slot 3 to _TOMBSTONE:
  [2] ("cat", 5)
  [3] _TOMBSTONE        ← "I'm gone, but keep going"
  [4] ("bird", 7)

Now try to find "bird":
  hash("bird") → 2 → found "cat", not a match
  probe → 3 → TOMBSTONE → skip, keep probing
  probe → 4 → found "bird" ✓
```

Now that you understand tombstones, **go back and update your `put` and `get` methods:**
- **`put`**: treat `_TOMBSTONE` the same as `None` — it's an open slot you can insert into
- **`get`**: when you see a `_TOMBSTONE`, skip over it and keep probing (don't stop like you would for `None`)

**Your algorithm for delete:**
1. Start at `_hash(key)`, probe forward (same as `get`)
2. If you find the matching key → replace the slot with `_TOMBSTONE`, decrement count
3. If you hit `None` or exhaust the table → raise `KeyError`

```bash
pytest -v -k "TestDelete"
git add -A && git commit -m "Lab 9: Implement delete with tombstones"
```

## Part 3: Write Your Own Tests

Open `tests/test_tombstones.py`. You'll find three test functions with descriptions but no code. Your job is to write the test implementations. Each one tests a specific tombstone behavior:

1. **Probe chain survives deletion** — insert keys that collide, delete one in the middle, verify you can still find the one after it
2. **Tombstone slot gets reused** — delete a key, insert a new key that would probe to the same slot, verify the table size didn't grow unnecessarily
3. **Count stays correct** — delete and reinsert keys, check `len()` at each step

Read the docstrings in the file — they describe exactly what to test.

**How to write a test:** Every test follows the same pattern:
```python
def test_something(self):
    ht = HashTableOpen(size=5)    # 1. Create a table
    ht.put("a", 1)                # 2. Do some operations
    ht.delete("a")
    assert ht.get("b") == 2       # 3. Assert the expected result
```

Use `assert` to check values, `assert "key" in ht` or `assert "key" not in ht` for membership, and `assert len(ht) == N` for count. Look at the tests in `test_hash_table.py` for more examples.

**Tip for forcing collisions:** Use a small table (like `size=3`). With only 3 slots, multiple keys are guaranteed to hash to the same index, which forces probing.

```bash
pytest -v -k "TestTombstones"
git add -A && git commit -m "Lab 9: Add tombstone tests"
```

## Part 4: Analysis Notebook

### Opening the Notebook in Colab

Once your notebook is pushed to GitHub, you can open it directly in Colab using this URL pattern:

```
https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/labs/Lab9/notebooks/analysis.ipynb
```

Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and repo name.

### Working in Colab

1. **First thing:** Click **File → Save a copy in Drive**. This gives you your own editable copy. Without this step, your work will disappear when you close the tab.
2. **Paste your code:** Copy your completed `HashTableOpen` class (including the `_TOMBSTONE = object()` line) from `src/hash_table_open.py` and paste it into the first code cell.
3. **Run each cell** and answer the questions in the markdown cells.

### What You'll Explore

The notebook has three experiments:

1. **Collision counting** — how many probes does it take to insert items as the table fills up? You'll see probe counts spike after ~75% full.
2. **Table visualization** — see your table as a color-coded bar chart (green = occupied, red = tombstone, gray = empty). Watch clusters form.
3. **Chaining vs probing** — side-by-side performance comparison. Which handles high load factors better, and why?

### Saving Back to GitHub

When you're done, save the notebook back to your repo:

1. **File → Save a copy in GitHub**
2. Colab will ask you to authorize with GitHub (one-time setup)
3. Select your repo and set the path to `labs/Lab9/notebooks/analysis.ipynb`
4. Click OK — Colab commits it directly to your repo

**Alternative:** If the GitHub save gives you trouble, use **File → Download .ipynb**, then upload the file to your repo through the GitHub website.

```bash
git pull   # if you saved from Colab, pull the changes
git add -A && git commit -m "Lab 9: Complete analysis notebook"
```

## Key Concepts

| Concept | What it means |
|---------|--------------|
| **Open addressing** | Every item lives in the table itself — no external lists |
| **Linear probing** | On collision, check the next slot, then the next, etc. |
| **Probe chain** | The sequence of slots checked when looking for a key |
| **Tombstone** | Marker for a deleted slot — "keep probing past me" |
| **Clustering** | Items clumping together, making probe chains longer |
| **Load factor limit** | Open addressing requires load factor < 1.0 (table can actually fill up) |

## Submission

Push your completed code and submit your repo URL.

Your commit history should look something like:
```
Lab 9: Organize project structure
Lab 9: Implement _hash
Lab 9: Implement put with linear probing
Lab 9: Implement get with probe search
Lab 9: Implement delete with tombstones
Lab 9: Add tombstone tests
Lab 9: Complete analysis notebook
```

```bash
git push
```
