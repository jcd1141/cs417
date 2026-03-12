"""Word counter using manual sys.argv parsing."""
import sys


def parse_args_manual(argv):
    """Extract filename from argv list.

    If no filename provided, print usage to stderr and exit with code 1.

    Args:
        argv: sys.argv (list of strings)

    Returns:
        str: the filename
    """
    # TODO: Check if argv has at least 2 elements (program name + filename)
    # If not, print "Usage: wordcount_manual.py <filename>" to stderr and exit(1)
    # Otherwise return argv[1]
    pass


def count_words(filepath):
    """Read a file and return the number of words.

    Words are defined by splitting on whitespace.

    Args:
        filepath: path to the text file

    Returns:
        int: total word count

    Raises:
        FileNotFoundError: prints error to stderr and exits with code 1
    """
    # TODO: Try to open and read the file
    # If FileNotFoundError, print "Error: file '<filepath>' not found" to stderr and exit(1)
    # Otherwise split on whitespace and return the count
    pass


def main():
    """Wire it together: parse args, count words, print result."""
    # TODO: Call parse_args_manual with sys.argv
    # Call count_words with the filename
    # Print "<filename>: <count> words"
    pass


if __name__ == "__main__":
    main()