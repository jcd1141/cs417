"""
Tests for Lab 14: BST Traversals

Run: pytest -v
"""

import pytest
from bst import BST
from traversals import (
    build_sample_tree,
    explore,
    inorder,
    preorder,
    postorder,
    levelorder,
)


# ── Helpers ──────────────────────────────────────────────────────────

@pytest.fixture
def sample_tree():
    """The sample tree from the lab: 15, 9, 21, 4, 12, 18, 25, 2, 7."""
    return build_sample_tree()


@pytest.fixture
def small_tree():
    """A small 3-node tree for basic checks."""
    tree = BST()
    for v in [10, 5, 20]:
        tree.insert(v)
    return tree


@pytest.fixture
def single_node():
    """A tree with just one node."""
    tree = BST()
    tree.insert(42)
    return tree


# ── Task 1: Explore ─────────────────────────────────────────────────

class TestExplore:
    """Basic check that explore() runs without error."""

    def test_explore_runs(self, capsys):
        explore()
        output = capsys.readouterr().out
        # Should print something about the tree
        assert "12" in output, "explore() should print search results"
        assert "9" in output, "explore() should show the tree or search results"


# ── Task 2: Inorder ─────────────────────────────────────────────────

class TestInorder:
    """Inorder: Left → Self → Right. Should produce sorted output."""

    def test_sample_tree(self, sample_tree):
        result = inorder(sample_tree.root)
        assert result == [2, 4, 7, 9, 12, 15, 18, 21, 25]

    def test_produces_sorted_output(self, sample_tree):
        result = inorder(sample_tree.root)
        assert result == sorted(result), "Inorder on a BST should produce sorted output"

    def test_small_tree(self, small_tree):
        result = inorder(small_tree.root)
        assert result == [5, 10, 20]

    def test_single_node(self, single_node):
        result = inorder(single_node.root)
        assert result == [42]

    def test_empty_tree(self):
        assert inorder(None) == []


# ── Task 3: Preorder ────────────────────────────────────────────────

class TestPreorder:
    """Preorder: Self → Left → Right. Root always comes first."""

    def test_sample_tree(self, sample_tree):
        result = preorder(sample_tree.root)
        assert result == [15, 9, 4, 2, 7, 12, 21, 18, 25]

    def test_root_is_first(self, sample_tree):
        result = preorder(sample_tree.root)
        assert result[0] == 15, "Preorder should visit the root first"

    def test_small_tree(self, small_tree):
        result = preorder(small_tree.root)
        assert result == [10, 5, 20]

    def test_single_node(self, single_node):
        result = preorder(single_node.root)
        assert result == [42]

    def test_empty_tree(self):
        assert preorder(None) == []


# ── Task 4: Postorder ───────────────────────────────────────────────

class TestPostorder:
    """Postorder: Left → Right → Self. Root always comes last."""

    def test_sample_tree(self, sample_tree):
        result = postorder(sample_tree.root)
        assert result == [2, 7, 4, 12, 9, 18, 25, 21, 15]

    def test_root_is_last(self, sample_tree):
        result = postorder(sample_tree.root)
        assert result[-1] == 15, "Postorder should visit the root last"

    def test_small_tree(self, small_tree):
        result = postorder(small_tree.root)
        assert result == [5, 20, 10]

    def test_single_node(self, single_node):
        result = postorder(single_node.root)
        assert result == [42]

    def test_empty_tree(self):
        assert postorder(None) == []


# ── Task 5: Level-Order ─────────────────────────────────────────────

class TestLevelorder:
    """Level-order: BFS, layer by layer. Uses a queue, not recursion."""

    def test_sample_tree(self, sample_tree):
        result = levelorder(sample_tree.root)
        assert result == [15, 9, 21, 4, 12, 18, 25, 2, 7]

    def test_first_level(self, sample_tree):
        result = levelorder(sample_tree.root)
        assert result[0] == 15, "Level-order should visit root first"
        assert result[1] == 9, "Level 1 left should come before level 1 right"
        assert result[2] == 21, "Level 1 right should come second on its level"

    def test_small_tree(self, small_tree):
        result = levelorder(small_tree.root)
        assert result == [10, 5, 20]

    def test_single_node(self, single_node):
        result = levelorder(single_node.root)
        assert result == [42]

    def test_empty_tree(self):
        assert levelorder(None) == []


# ── Cross-Traversal Checks ──────────────────────────────────────────

class TestCrossTraversal:
    """Verify that all traversals visit every node exactly once."""

    def test_all_same_elements(self, sample_tree):
        root = sample_tree.root
        expected = {2, 4, 7, 9, 12, 15, 18, 21, 25}

        assert set(inorder(root)) == expected
        assert set(preorder(root)) == expected
        assert set(postorder(root)) == expected
        assert set(levelorder(root)) == expected

    def test_all_same_length(self, sample_tree):
        root = sample_tree.root

        assert len(inorder(root)) == 9
        assert len(preorder(root)) == 9
        assert len(postorder(root)) == 9
        assert len(levelorder(root)) == 9

    def test_all_different_orders(self, sample_tree):
        """The four traversals should produce different orderings."""
        root = sample_tree.root
        results = [
            inorder(root),
            preorder(root),
            postorder(root),
            levelorder(root),
        ]
        # All four should be different from each other
        for i in range(len(results)):
            for j in range(i + 1, len(results)):
                assert results[i] != results[j], (
                    f"Traversals {i} and {j} produced the same order — "
                    "each traversal should visit nodes in a different sequence"
                )