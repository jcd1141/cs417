"""
Pytest configuration — adds src/ to the import path.

This file lets pytest find your code in src/ when tests
are in tests/. Keep this file in the Lab9 root directory.
"""

import sys
import os

# Add src/ to Python's module search path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
