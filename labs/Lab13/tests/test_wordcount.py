"""Tests for Lab 13: Building Command-Line Tools with argparse."""
import subprocess
import sys
from pathlib import Path

import pytest

# Paths
LAB_ROOT = Path(__file__).parent.parent
SRC = LAB_ROOT / "src"
DATA = LAB_ROOT / "data"
SAMPLE = DATA / "sample.txt"

# Precompute expected values from sample.txt
# "the quick brown fox jumps over the lazy dog\n..."
SAMPLE_WORDS = SAMPLE.read_text().split()
SAMPLE_COUNT = len(SAMPLE_WORDS)


def run_script(script_name, *args):
    """Run a script in src/ and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(SRC / script_name), *args],
        capture_output=True, text=True, timeout=10,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


# ============================================================
# Task 1: Manual sys.argv parsing
# ============================================================

class TestManual:
    """Tests for wordcount_manual.py (sys.argv version)."""

    def test_counts_words(self):
        """Basic word count on sample file."""
        code, out, err = run_script("wordcount_manual.py", str(SAMPLE))
        assert code == 0
        assert f"{SAMPLE_COUNT} words" in out

    def test_missing_filename_shows_usage(self):
        """No arguments → usage message and exit code 1."""
        code, out, err = run_script("wordcount_manual.py")
        assert code == 1
        assert "Usage" in err or "usage" in err

    def test_nonexistent_file_shows_error(self):
        """Bad filename → error message and exit code 1."""
        code, out, err = run_script("wordcount_manual.py", "nonexistent.txt")
        assert code == 1
        assert "not found" in err.lower() or "error" in err.lower()

    def test_output_format(self):
        """Output includes filename and word count."""
        code, out, err = run_script("wordcount_manual.py", str(SAMPLE))
        assert code == 0
        # Should contain the filename (or at least the basename) and count
        assert str(SAMPLE_COUNT) in out


# ============================================================
# Task 2: argparse version — basic functionality
# ============================================================

class TestArgparse:
    """Tests for wordcount.py basic argparse features."""

    def test_counts_words(self):
        """Basic word count on sample file."""
        code, out, err = run_script("wordcount.py", str(SAMPLE))
        assert code == 0
        assert f"{SAMPLE_COUNT} words" in out

    def test_help_flag(self):
        """--help produces help text and exits cleanly."""
        code, out, err = run_script("wordcount.py", "--help")
        assert code == 0
        assert "filename" in out.lower()

    def test_missing_filename_exits_nonzero(self):
        """No arguments → argparse shows error and exits nonzero."""
        code, out, err = run_script("wordcount.py")
        assert code != 0

    def test_nonexistent_file(self):
        """Bad filename → error."""
        code, out, err = run_script("wordcount.py", "nonexistent.txt")
        assert code != 0

    def test_ignore_case(self):
        """--ignore-case doesn't change total count but affects top words."""
        code, out, err = run_script("wordcount.py", str(SAMPLE), "--ignore-case")
        assert code == 0
        assert f"{SAMPLE_COUNT} words" in out

    def test_top_flag(self):
        """--top N shows the N most frequent words."""
        code, out, err = run_script("wordcount.py", str(SAMPLE), "--top", "3")
        assert code == 0
        assert "Top 3 words" in out
        # "the" should be the most frequent word
        assert "the" in out

    def test_top_with_ignore_case(self):
        """--top combined with --ignore-case."""
        code, out, err = run_script(
            "wordcount.py", str(SAMPLE), "--top", "3", "--ignore-case"
        )
        assert code == 0
        assert "Top 3 words" in out

    def test_top_format(self):
        """Top words output has indented word: count lines."""
        code, out, err = run_script("wordcount.py", str(SAMPLE), "--top", "2")
        assert code == 0
        lines = out.split("\n")
        # Find lines that look like "  word: N"
        top_lines = [l for l in lines if l.startswith("  ") and ":" in l]
        assert len(top_lines) == 2


# ============================================================
# Task 3: Extended flags
# ============================================================

class TestExtended:
    """Tests for extended argparse features."""

    def test_min_length_filters(self):
        """--min-length filters short words."""
        code, out, err = run_script(
            "wordcount.py", str(SAMPLE), "--min-length", "4"
        )
        assert code == 0
        # Count should be less than total (filters "the", "a", "at", etc.)
        # Extract the number from output
        count = int(out.split(":")[1].split("words")[0].strip())
        assert count < SAMPLE_COUNT

    def test_min_length_with_top(self):
        """--min-length combined with --top."""
        code, out, err = run_script(
            "wordcount.py", str(SAMPLE), "--min-length", "4", "--top", "3"
        )
        assert code == 0
        assert "Top 3 words" in out
        # "the" (3 chars) should NOT appear in top words
        top_lines = [l.strip() for l in out.split("\n") if l.startswith("  ") and ":" in l]
        top_words = [l.split(":")[0].strip() for l in top_lines]
        assert "the" not in top_words

    def test_sort_by_alpha(self):
        """--sort-by alpha sorts top words alphabetically."""
        code, out, err = run_script(
            "wordcount.py", str(SAMPLE), "--top", "5", "--sort-by", "alpha"
        )
        assert code == 0
        top_lines = [l.strip() for l in out.split("\n") if l.startswith("  ") and ":" in l]
        assert len(top_lines) == 5
        top_words = [l.split(":")[0].strip() for l in top_lines]
        assert top_words == sorted(top_words)

    def test_sort_by_freq_default(self):
        """Default sort is by frequency (descending)."""
        code, out, err = run_script(
            "wordcount.py", str(SAMPLE), "--top", "3"
        )
        assert code == 0
        top_lines = [l.strip() for l in out.split("\n") if l.startswith("  ") and ":" in l]
        assert len(top_lines) == 3
        counts = [int(l.split(":")[1].strip()) for l in top_lines]
        assert counts == sorted(counts, reverse=True)

    def test_reverse_flag(self):
        """--reverse flips the sort order."""
        code, out, err = run_script(
            "wordcount.py", str(SAMPLE), "--top", "5", "--sort-by", "alpha", "--reverse"
        )
        assert code == 0
        top_lines = [l.strip() for l in out.split("\n") if l.startswith("  ") and ":" in l]
        assert len(top_lines) == 5
        top_words = [l.split(":")[0].strip() for l in top_lines]
        assert top_words == sorted(top_words, reverse=True)

    def test_reverse_freq(self):
        """--reverse with freq sort shows least frequent first."""
        code, out, err = run_script(
            "wordcount.py", str(SAMPLE), "--top", "3", "--reverse"
        )
        assert code == 0
        top_lines = [l.strip() for l in out.split("\n") if l.startswith("  ") and ":" in l]
        assert len(top_lines) == 3
        counts = [int(l.split(":")[1].strip()) for l in top_lines]
        assert counts == sorted(counts)

    def test_invalid_sort_by_rejected(self):
        """--sort-by with invalid choice is rejected by argparse."""
        code, out, err = run_script(
            "wordcount.py", str(SAMPLE), "--sort-by", "invalid"
        )
        assert code != 0

    def test_all_flags_together(self):
        """All flags combined work without error."""
        code, out, err = run_script(
            "wordcount.py", str(SAMPLE),
            "--top", "3", "--ignore-case", "--min-length", "3",
            "--sort-by", "alpha", "--reverse"
        )
        assert code == 0
        assert "Top 3 words" in out