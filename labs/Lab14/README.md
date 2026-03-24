# Lab 14: Walking Trees — BST Traversals

## Overview

Every data structure you've worked with so far has been flat — arrays, linked lists, hash tables. You put things in, you get things out, and the structure is basically a line. Trees are different. Trees are **hierarchical** — every node can branch, and the path you take through the tree changes what you see and when you see it.

In this lab, you'll work with a **Binary Search Tree (BST)** that's already built for you. Your job isn't to build the tree — it's to **walk** it. You'll implement four different traversal algorithms, each of which visits every node but in a completely different order. Same tree, four different walks, four different outputs. Understanding *why* each order matters is the point.

**Starter files:** `bst.py` (provided — don't modify), `traversals.py`, `predictions.py`, `test_traversals.py`, `conftest.py`
**Test command:** `pytest -v` (from your Lab14 root)

## Part 1: Project Setup

```
Lab14/
├── README.md
├── conftest.py
├── src/
│   ├── bst.py
│   ├── traversals.py
│   └── predictions.py
├── tests/
│   └── test_traversals.py
```

1. Create the `src/` and `tests/` directories
2. Move files into their places
3. Verify: `pytest -v` — all tests should **fail** (except any prediction tests, which won't run until you fill them in)

```bash
git add -A && git commit -m "Lab 14: Organize project structure"
```

## Background: Trees and Hierarchy

A **tree** is a data structure where each node can have children. A **binary tree** means each node has at most two children — a left child and a right child.

A **Binary Search Tree** adds one rule: for every node, everything in its left subtree is smaller, and everything in its right subtree is larger. That single rule is what makes searching fast — at each node, you know which direction to go.

Here's a BST built by inserting the values `15, 9, 21, 4, 12, 18, 25, 2, 7` in that order:

```
         15
        /  \
       9    21
      / \   / \
     4  12 18  25
    / \
   2   7
```

Notice: every value to the left of 15 is smaller. Every value to the right is larger. And that rule holds at *every* node, not just the root.

You won't build this tree yourself. The `bst.py` module handles insertion, searching, and display. You'll import it and focus on the interesting question: **how do you visit every node, and why does the visit order matter?**

## Part 2: Meet the Tree

Open `src/traversals.py`. At the top, you'll see how to import and use the BST module.

### Task 1: Explore the BST

Get comfortable with the provided BST module. In `traversals.py`, there's a `build_sample_tree()` function that's already done for you — it builds the tree from the diagram above.

**Your task:** Fill in `explore()` to do the following:
- Build the sample tree using `build_sample_tree()`
- Print the tree using its `display()` method
- Search for the values `12`, `20`, and `25` — for each, print whether it was found
- Print the total number of nodes in the tree (use the `size()` method)

Run it:
```bash
python src/traversals.py
```

You should see the tree structure printed, search results for all three values, and the node count. Look at the shape. Notice where values ended up. Why is `9` to the left of `15`? Why is `7` to the right of `4` but to the left of `9`?

```bash
pytest -v -k "TestExplore"
git add -A && git commit -m "Lab 14: Explore the BST"
```

## Part 3: Predict the Traversals

Before you write any traversal code, you're going to **predict** what each traversal produces. This is where the conceptual understanding happens — tracing through the tree in your head, following the rules, and seeing what comes out.

Open `src/predictions.py`. You'll see the tree diagram and four empty lists. Fill in each list with the order you think that traversal will visit the nodes.

Here are the rules for each traversal:

**Inorder** (Left → Self → Right): At each node, visit the entire left subtree first, then the current node, then the entire right subtree.

**Preorder** (Self → Left → Right): At each node, visit the current node first, then the entire left subtree, then the entire right subtree.

**Postorder** (Left → Right → Self): At each node, visit the entire left subtree, then the entire right subtree, then the current node last.

**Level-order** (Top → Bottom, Left → Right): Visit every node on level 0, then every node on level 1, then level 2, and so on. Within each level, go left to right.

Fill in all four prediction lists in `predictions.py`, then run:
```bash
python src/predictions.py
```

It will check each prediction against the actual traversal and tell you which ones you got right. If you got any wrong, trace through the tree again before moving on. Don't just correct the list to match the output — figure out *where* your mental trace went wrong.

```bash
git add -A && git commit -m "Lab 14: Traversal predictions"
```

## Background: Why Four Walks?

It might seem strange that we need four ways to visit the same nodes. But each traversal answers a different question:

- **Inorder** gives you the values in **sorted order**. This is the BST payoff — the structure *is* the sort. If you walk it inorder, the data comes out sorted without any sorting algorithm.
- **Preorder** captures the **structure** of the tree. If you recorded a preorder traversal and rebuilt a BST by inserting values in that order, you'd get the exact same tree back. This is how you'd serialize a tree.
- **Postorder** processes **children before parents**. This is the order you'd use to safely delete a tree (remove leaves first, work your way up) or evaluate an expression tree (compute the operands before the operator).
- **Level-order** visits nodes by **distance from the root** — closest first. This is what you'd want for finding the shortest path, printing the tree layer by layer, or any "nearest first" search.

Same data. Different questions. Different walks.

## Part 4: Implement the Traversals

Now implement them for real. Open `src/traversals.py`. You'll find four functions to complete, each taking a BST node and returning a list of values in the correct order.

### Task 2: `inorder(node)` — Left, Self, Right

The recursive pattern: go left, collect the current value, go right.

- If the node is `None`, return an empty list
- Recursively traverse the left subtree
- Include the current node's value
- Recursively traverse the right subtree
- Return all values as a single list

**Hint:** Think about how you combine three things — the result from the left, the current value, and the result from the right — into one list.

```bash
pytest -v -k "TestInorder"
git add -A && git commit -m "Lab 14: Implement inorder traversal"
```

### Task 3: `preorder(node)` — Self, Left, Right

Same structure as inorder, but the current node comes **first**.

- If the node is `None`, return an empty list
- Start with the current node's value
- Then the left subtree
- Then the right subtree

```bash
pytest -v -k "TestPreorder"
git add -A && git commit -m "Lab 14: Implement preorder traversal"
```

### Task 4: `postorder(node)` — Left, Right, Self

And here the current node comes **last**.

- If the node is `None`, return an empty list
- Left subtree first
- Then right subtree
- Then the current node's value

```bash
pytest -v -k "TestPostorder"
git add -A && git commit -m "Lab 14: Implement postorder traversal"
```

### Task 5: `levelorder(node)` — The Odd One Out

This one is different. The first three traversals are all recursive — they use the call stack to remember where they've been. Level-order doesn't work that way. It visits nodes **layer by layer**, left to right, and it uses a **queue** instead of recursion.

The algorithm:
1. Start with a queue containing just the root node
2. While the queue isn't empty:
   - Remove the node at the **front** of the queue
   - Record its value
   - Add its left child to the queue (if it exists)
   - Add its right child to the queue (if it exists)
3. Return all recorded values

**Why a queue?** Because a queue is first-in, first-out. When you add a node's children to the back of the line, they wait until every node on the current level has been processed. That's what gives you the level-by-level order.

**Hint:** Python's `collections.deque` works great as a queue — `append()` adds to the back, `popleft()` removes from the front.

```bash
pytest -v -k "TestLevelorder"
git add -A && git commit -m "Lab 14: Implement level-order traversal"
```

## Key Concepts

| Concept | What it means |
|---------|--------------|
| **Binary Search Tree** | A binary tree where left < parent < right at every node |
| **Traversal** | A systematic way to visit every node in a tree |
| **Inorder** | Left → Self → Right — produces sorted output from a BST |
| **Preorder** | Self → Left → Right — captures tree structure |
| **Postorder** | Left → Right → Self — processes children before parents |
| **Level-order** | Layer by layer, top to bottom — uses a queue, not recursion |
| **Recursive traversal** | Uses the call stack to track position (inorder, preorder, postorder) |
| **Queue-based traversal** | Uses an explicit queue to process nodes in FIFO order (level-order) |

## Submission

Push your completed code and submit your repo URL.

Your commit history should look something like:
```
Lab 14: Organize project structure
Lab 14: Explore the BST
Lab 14: Traversal predictions
Lab 14: Implement inorder traversal
Lab 14: Implement preorder traversal
Lab 14: Implement postorder traversal
Lab 14: Implement level-order traversal
```

```bash
git push
```