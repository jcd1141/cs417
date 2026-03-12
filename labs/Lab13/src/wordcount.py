"""Word counter using argparse."""
import argparse
from collections import Counter


def build_parser():
    """Create and return the argument parser.

    Arguments to define:
        filename    - positional, the text file to analyze
        --ignore-case / -i  - store_true, lowercase all words
        --top / -t          - int, show top N most frequent words (default: None)
        --min-length / -m   - int, only count words with at least this many chars (default: 1)
        --sort-by / -s      - choices ["freq", "alpha"], how to sort top words (default: "freq")
        --reverse / -r      - store_true, reverse the sort order

    Returns:
        argparse.ArgumentParser
    """
    # TODO: Create an ArgumentParser with a description
    # TODO: Add the positional 'filename' argument
    # TODO: Add --ignore-case / -i (action="store_true")
    # TODO: Add --top / -t (type=int, default=None)
    # TODO: Add --min-length / -m (type=int, default=1)
    # TODO: Add --sort-by / -s (choices=["freq", "alpha"], default="freq")
    # TODO: Add --reverse / -r (action="store_true")
    pass


def analyze(filepath, ignore_case=False, top=None, min_length=1,
            sort_by="freq", reverse=False):
    """Analyze a text file and return a formatted result string.

    Args:
        filepath: path to the text file
        ignore_case: if True, lowercase all words before counting
        top: if set, show the N most frequent words with counts
        min_length: only count words with at least this many characters
        sort_by: "freq" (by count) or "alpha" (alphabetical) when showing top words
        reverse: if True, reverse the sort order

    Returns:
        str: formatted result

    Raises:
        FileNotFoundError: if the file doesn't exist
    """
    # TODO: Read the file and split into words on whitespace
    # TODO: If ignore_case, lowercase all words
    # TODO: Filter out words shorter than min_length
    # TODO: Count total words
    # TODO: If top is None, return "<filename>: <count> words"
    # TODO: If top is set, find the most frequent words:
    #   - Use Counter(words).most_common() for frequency data
    #   - If sort_by == "alpha", sort alphabetically instead
    #   - If reverse, flip the order
    #   - Take the first 'top' entries
    #   - Return multi-line string:
    #       "<filename>: <count> words\n\nTop <N> words:\n  <word>: <count>\n  ..."
    pass


def main():
    """Build parser, parse args, analyze, print result."""
    # TODO: Build the parser
    # TODO: Parse args
    # TODO: Call analyze with the parsed arguments
    # TODO: Print the result
    pass


if __name__ == "__main__":
    main()