"""
Binary Search Tree — provided module.
DO NOT MODIFY this file. Use it as-is in your traversals.

Usage:
    from bst import BST

    tree = BST()
    tree.insert(15)
    tree.insert(9)
    tree.search(9)       # Returns the node
    tree.search(99)      # Returns None
    tree.size()          # Returns number of nodes
    tree.display()       # Prints the tree structure
    tree.root            # The root Node (has .value, .left, .right)
"""


class Node:
    """A single node in the BST."""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.value})"


class BST:
    """Binary Search Tree with insert, search, size, and display."""

    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insert a value into the BST."""
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert(node.right, value)
        # Duplicate values are ignored

    def search(self, value):
        """Search for a value. Returns the Node if found, None otherwise."""
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return None
        if value == node.value:
            return node
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    def size(self):
        """Return the number of nodes in the tree."""
        return self._size(self.root)

    def _size(self, node):
        if node is None:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)

    def display(self):
        """Print a visual representation of the tree."""
        lines = self._build_display(self.root)
        for line in lines:
            print(line)

    def _build_display(self, node):
        """Build a list of strings representing the tree structure."""
        if node is None:
            return []

        # Leaf node
        if node.left is None and node.right is None:
            return [str(node.value)]

        # Only right child
        if node.left is None:
            right_lines = self._build_display(node.right)
            first_line = str(node.value) + " ──┐"
            gap = " " * len(str(node.value)) + "   "
            connector = " " * len(str(node.value)) + "   "
            result = [first_line]
            for i, line in enumerate(right_lines):
                if i == 0:
                    result.append(connector + "└── " + line)
                else:
                    result.append(gap + "    " + line)
            return result

        # Only left child
        if node.right is None:
            left_lines = self._build_display(node.left)
            first_line = str(node.value) + " ──┐"
            gap = " " * len(str(node.value)) + "   "
            connector = " " * len(str(node.value)) + "   "
            result = [first_line]
            for i, line in enumerate(left_lines):
                if i == 0:
                    result.append(connector + "├── " + line)
                else:
                    result.append(gap + "│   " + line)
            return result

        # Both children — use a simpler indented format
        left_lines = self._build_display(node.left)
        right_lines = self._build_display(node.right)
        val = str(node.value)
        pad = " " * len(val)

        result = [val]
        # Left subtree
        for i, line in enumerate(left_lines):
            if i == 0:
                result.append(pad + " ├─L─ " + line)
            else:
                result.append(pad + " │    " + line)
        # Right subtree
        for i, line in enumerate(right_lines):
            if i == 0:
                result.append(pad + " └─R─ " + line)
            else:
                result.append(pad + "      " + line)

        return result