"""
Traversal Predictions — Lab 14

Fill in your predicted traversal orders for the sample BST,
then run this file to check your answers.

Tree (built by inserting 15, 9, 21, 4, 12, 18, 25, 2, 7):

         15
        /  \\
       9    21
      / \\   / \\
     4  12 18  25
    / \\
   2   7

Rules:
  Inorder:     Left → Self → Right
  Preorder:    Self → Left → Right
  Postorder:   Left → Right → Self
  Level-order: Top → Bottom, Left → Right (layer by layer)
"""

from bst import BST
from collections import deque

# ── Your Predictions ─────────────────────────────────────────────────
# Fill in each list with the order you think that traversal visits nodes.
# Use the integer values (e.g., [15, 9, 4, ...]).

inorder_prediction = []       # TODO: fill in your prediction
preorder_prediction = []      # TODO: fill in your prediction
postorder_prediction = []     # TODO: fill in your prediction
levelorder_prediction = []    # TODO: fill in your prediction


# ── Checking (don't modify below this line) ──────────────────────────

def _inorder(node):
    if node is None:
        return []
    return _inorder(node.left) + [node.value] + _inorder(node.right)


def _preorder(node):
    if node is None:
        return []
    return [node.value] + _preorder(node.left) + _preorder(node.right)


def _postorder(node):
    if node is None:
        return []
    return _postorder(node.left) + _postorder(node.right) + [node.value]


def _levelorder(node):
    if node is None:
        return []
    result = []
    queue = deque([node])
    while queue:
        current = queue.popleft()
        result.append(current.value)
        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)
    return result


def check():
    tree = BST()
    for v in [15, 9, 21, 4, 12, 18, 25, 2, 7]:
        tree.insert(v)

    checks = [
        ("Inorder", inorder_prediction, _inorder(tree.root)),
        ("Preorder", preorder_prediction, _preorder(tree.root)),
        ("Postorder", postorder_prediction, _postorder(tree.root)),
        ("Level-order", levelorder_prediction, _levelorder(tree.root)),
    ]

    all_correct = True
    for name, predicted, actual in checks:
        if not predicted:
            print(f"  {name}: (empty — fill in your prediction first)")
            all_correct = False
        elif predicted == actual:
            print(f"  {name}: ✓ Correct!")
        else:
            print(f"  {name}: ✗ Not quite.")
            print(f"    Your prediction: {predicted}")
            print(f"    Actual:          {actual}")
            print(f"    Trace through the tree again — where did your path diverge?")
            all_correct = False

    if all_correct:
        print("\nAll four correct — nice work! You're ready to implement them.")


if __name__ == "__main__":
    print("Checking your traversal predictions...\n")
    check()