"""
Tests for Open Addressing Hash Table — Lab 9.
Do not modify this file.

Run from the Lab9 directory:
    pytest -v
"""

from hash_table_open import HashTableOpen


# ═══════════════════════════════════════════════════════════════════
# Task 1 Tests: Hash Function
# ═══════════════════════════════════════════════════════════════════


class TestHashFunction:
    """Tests that _hash returns valid slot indices."""

    def test_returns_int(self):
        ht = HashTableOpen(size=10)
        assert isinstance(ht._hash("hello"), int)

    def test_within_range(self):
        ht = HashTableOpen(size=10)
        for key in ["apple", "banana", "cherry", 42, 99, "z"]:
            idx = ht._hash(key)
            assert 0 <= idx < 10, f"_hash({key!r}) returned {idx}, expected 0-9"

    def test_consistent(self):
        ht = HashTableOpen(size=10)
        assert ht._hash("test") == ht._hash("test")


# ═══════════════════════════════════════════════════════════════════
# Task 2 Tests: Put
# ═══════════════════════════════════════════════════════════════════


class TestPut:
    """Tests for inserting key-value pairs with linear probing."""

    def test_put_and_get_one(self):
        ht = HashTableOpen()
        ht.put("name", "Alice")
        assert ht.get("name") == "Alice"

    def test_put_and_get_multiple(self):
        ht = HashTableOpen()
        ht.put("a", 1)
        ht.put("b", 2)
        ht.put("c", 3)
        assert ht.get("a") == 1
        assert ht.get("b") == 2
        assert ht.get("c") == 3

    def test_update_existing_key(self):
        ht = HashTableOpen()
        ht.put("color", "red")
        ht.put("color", "blue")
        assert ht.get("color") == "blue"

    def test_count_increases(self):
        ht = HashTableOpen()
        assert len(ht) == 0
        ht.put("a", 1)
        assert len(ht) == 1
        ht.put("b", 2)
        assert len(ht) == 2

    def test_count_no_increase_on_update(self):
        ht = HashTableOpen()
        ht.put("a", 1)
        ht.put("a", 2)
        assert len(ht) == 1

    def test_probing_on_collision(self):
        """Force collisions with a tiny table."""
        ht = HashTableOpen(size=3)
        ht.put("a", 1)
        ht.put("b", 2)
        ht.put("c", 3)
        assert ht.get("a") == 1
        assert ht.get("b") == 2
        assert ht.get("c") == 3

    def test_full_table_raises(self):
        ht = HashTableOpen(size=2)
        ht.put("x", 1)
        ht.put("y", 2)
        try:
            ht.put("z", 3)
            assert False, "Expected Exception for full table"
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════
# Task 3 Tests: Get
# ═══════════════════════════════════════════════════════════════════


class TestGet:
    """Tests for looking up keys through probe chains."""

    def test_get_missing_raises(self):
        ht = HashTableOpen()
        ht.put("x", 10)
        try:
            ht.get("y")
            assert False, "Expected KeyError"
        except KeyError:
            pass

    def test_get_from_empty_table(self):
        ht = HashTableOpen()
        try:
            ht.get("anything")
            assert False, "Expected KeyError"
        except KeyError:
            pass

    def test_get_with_collisions(self):
        """Insert multiple items that collide, verify all are findable."""
        ht = HashTableOpen(size=3)
        ht.put("a", 10)
        ht.put("b", 20)
        ht.put("c", 30)
        # All three must be retrievable even though they share 3 slots
        assert ht.get("a") == 10
        assert ht.get("b") == 20
        assert ht.get("c") == 30

    def test_integer_keys(self):
        ht = HashTableOpen()
        ht.put(1, "one")
        ht.put(2, "two")
        assert ht.get(1) == "one"
        assert ht.get(2) == "two"


# ═══════════════════════════════════════════════════════════════════
# Task 4 Tests: Delete
# ═══════════════════════════════════════════════════════════════════


class TestDelete:
    """Tests for deleting keys with tombstones."""

    def test_delete_existing(self):
        ht = HashTableOpen()
        ht.put("x", 10)
        ht.delete("x")
        assert "x" not in ht

    def test_delete_decrements_count(self):
        ht = HashTableOpen()
        ht.put("a", 1)
        ht.put("b", 2)
        assert len(ht) == 2
        ht.delete("a")
        assert len(ht) == 1

    def test_delete_missing_raises(self):
        ht = HashTableOpen()
        try:
            ht.delete("ghost")
            assert False, "Expected KeyError"
        except KeyError:
            pass


# ═══════════════════════════════════════════════════════════════════
# Bonus Tests: Contains and Load Factor
# ═══════════════════════════════════════════════════════════════════


class TestContainsAndLoadFactor:
    """Tests for __contains__ and load_factor."""

    def test_contains_true(self):
        ht = HashTableOpen()
        ht.put("hello", "world")
        assert "hello" in ht

    def test_contains_false(self):
        ht = HashTableOpen()
        assert "missing" not in ht

    def test_load_factor_empty(self):
        ht = HashTableOpen(size=10)
        assert ht.load_factor() == 0.0

    def test_load_factor_half(self):
        ht = HashTableOpen(size=10)
        for i in range(5):
            ht.put(f"key_{i}", i)
        assert ht.load_factor() == 0.5
