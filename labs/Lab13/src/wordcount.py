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
    parser = argparse.ArgumentParser(description="Analyze word counts in a text file.")
    parser.add_argument("filename", help="text file to analyze")
    parser.add_argument("-i", "--ignore-case", action="store_true", default=False)
    parser.add_argument("-t", "--top", type=int, default=None)
    parser.add_argument("-m", "--min-length", type=int, default=1)
    parser.add_argument("-s", "--sort-by", choices=["freq", "alpha"], default="freq")
    parser.add_argument("-r", "--reverse", action="store_true", default=False)
    return parser



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
    with open(filepath, "r") as file:
        words = file.read().split()

    if ignore_case:
        words = [word.lower() for word in words]

    words = [word for word in words if len(word) >= min_length]
    count = len(words)

    if top is None:
        return f"{filepath}: {count} words"

    counter = Counter(words)
    items = list(counter.items())

    if sort_by == "freq":
        items.sort(key=lambda item: (-item[1], item[0]))
    else:
        items.sort(key=lambda item: item[0])

    if reverse:
        items.reverse()

    items = items[:top]

    lines = [f"{filepath}: {count} words", "", f"Top {top} words:"]
    for word, freq in items:
        lines.append(f"  {word}: {freq}")

    return "\n".join(lines)


def main():
    """Build parser, parse args, analyze, print result."""
    # TODO: Build the parser
    # TODO: Parse args
    # TODO: Call analyze with the parsed arguments
    # TODO: Print the result
    parser = build_parser()
    args = parser.parse_args()
    result = analyze(
        args.filename,
        ignore_case=args.ignore_case,
        top=args.top,
        min_length=args.min_length,
        sort_by=args.sort_by,
        reverse=args.reverse
    )
    print(result)


if __name__ == "__main__":
    main()