# Lab 13: Building Command-Line Tools with argparse

## Overview

Every lab so far, your code has worked on hardcoded data — lists typed directly into your source file or test cases. Real tools don't work that way. Real tools take input from the command line: file paths, options, flags. Every professional Python script you'll encounter (or ask an LLM to write) uses a proper argument parser.

In this lab, you'll build a word-counting tool twice. First the hard way — parsing arguments manually with `sys.argv`. Then the right way — using Python's `argparse` module. By the end, you'll see why argparse is the standard: you describe what your CLI *should* look like, and it handles the rest.

**Starter files:** `wordcount_manual.py`, `wordcount.py`, `test_wordcount.py`, `sample.txt`
**Test command:** `pytest -v` (from your Lab13 root)

## Part 1: Project Setup

```
Lab13/
├── README.md
├── conftest.py
├── src/
│   ├── wordcount_manual.py
│   └── wordcount.py
├── tests/
│   └── test_wordcount.py
└── data/
    └── sample.txt
```

1. Create the `src/`, `tests/`, and `data/` directories
2. Move files into their places
3. Verify: `pytest -v` — all tests should **fail**

```bash
git add -A && git commit -m "Lab 13: Organize project structure"
```

## Background: How Scripts Take Input

When you run a command like:
```bash
python wordcount.py report.txt --top 5 --ignore-case
```

Python stores everything after `python` in a list called `sys.argv`:
```python
['wordcount.py', 'report.txt', '--top', '5', '--ignore-case']
```

That's it — just a list of strings. No types, no validation, no help text. If you want `5` to be an integer, you convert it yourself. If someone forgets the filename, your script crashes with an ugly IndexError. If someone types `--help`, nothing happens.

This is where `argparse` comes in. Instead of picking through a string list, you *declare* what arguments your tool expects — names, types, defaults, help text — and argparse handles parsing, validation, error messages, and `--help` for free.

## Part 2: The Hard Way — `sys.argv`

Open `src/wordcount_manual.py`. You'll find a `main()` function with TODOs.

### Task 1: Manual Argument Parsing

Build a word counter that reads a file and prints the total word count. Use only `sys.argv` — no argparse.

**Requirements:**
- The filename comes from `sys.argv[1]`
- If no filename is provided, print `"Usage: wordcount_manual.py <filename>"` to stderr and exit with code 1
- If the file doesn't exist, print `"Error: file '<filename>' not found"` to stderr and exit with code 1
- Read the file, split on whitespace, print the count: `"<filename>: <count> words"`

**The starter code gives you the structure.** Fill in:
- `parse_args_manual(argv)` — extract filename from argv, return it (or print usage and exit)
- `count_words(filepath)` — read the file, return the word count
- `main()` — wire them together

Try running it when you're done:
```bash
python src/wordcount_manual.py data/sample.txt
python src/wordcount_manual.py                    # should show usage
python src/wordcount_manual.py nonexistent.txt    # should show error
```

Notice what you had to handle manually: checking length of argv, printing your own usage message, your own error messages. And this is the *simple* version — we haven't even added flags yet.

```bash
pytest -v -k "TestManual"
git add -A && git commit -m "Lab 13: Implement manual sys.argv word counter"
```

## Part 3: The Right Way — `argparse`

Open `src/wordcount.py`. Same tool, rebuilt with argparse.

### Task 2: argparse Word Counter

Rebuild the word counter using `argparse`. Same core behavior, but now with proper argument handling.

**Fill in `build_parser()`** — create and return an `ArgumentParser` with:
- **Positional argument**: `filename` — the text file to analyze (help: `"text file to analyze"`)
- **Optional flag**: `--ignore-case` / `-i` — convert all words to lowercase before counting (default: False)
- **Optional argument**: `--top` / `-t` — only show the N most frequent words, with counts (type: int, default: None)

**Fill in `analyze(filepath, ignore_case=False, top=None)`** — this does the real work:
- Read the file and split into words on whitespace
- If `ignore_case` is True, lowercase everything
- If `top` is None: return the string `"<filename>: <count> words"`
- If `top` is provided: find the N most frequent words and return a multi-line string:
  ```
  <filename>: <count> words

  Top <N> words:
    <word1>: <count1>
    <word2>: <count2>
    ...
  ```

**Hint for counting frequency:** Python's `collections.Counter` is perfect here — `Counter(words).most_common(n)` gives you the top N as a list of `(word, count)` tuples.

**Fill in `main()`** — build the parser, parse args, call analyze, print the result.

Try it:
```bash
python src/wordcount.py data/sample.txt
python src/wordcount.py data/sample.txt --top 5
python src/wordcount.py data/sample.txt --top 5 --ignore-case
python src/wordcount.py --help
```

That `--help` output? You got it for free. Try giving it a nonexistent file — argparse doesn't catch that (it's not a file type), so your `analyze` function should raise `FileNotFoundError`.

```bash
pytest -v -k "TestArgparse"
git add -A && git commit -m "Lab 13: Implement argparse word counter"
```

## Part 4: Extending the Tool

### Task 3: More Flags

Add three more options to your argparse tool. This is where you see argparse scale — adding a flag is a few lines, not a rewrite of your parsing logic.

**Add to `build_parser()`:**
- `--min-length` / `-m` — only count words with at least this many characters (type: int, default: 1)
- `--sort-by` / `-s` — when showing top words, sort by `"freq"` (default) or `"alpha"` (choices: `["freq", "alpha"]`)
- `--reverse` / `-r` — reverse the sort order (default: False)

**Update `analyze()`** to accept and handle the new parameters:
- `min_length`: filter out words shorter than this before counting
- `sort_by`: when `top` is specified, `"freq"` sorts by count (most frequent first), `"alpha"` sorts alphabetically
- `reverse`: flip the sort order

**Example:**
```bash
# Top 5 words, at least 4 characters, sorted alphabetically
python src/wordcount.py data/sample.txt --top 5 --min-length 4 --sort-by alpha

# Same but reversed
python src/wordcount.py data/sample.txt --top 5 --min-length 4 --sort-by alpha --reverse
```

Think about how you'd add these three options with `sys.argv`. You'd need to scan for `--min-length`, find the next element, convert it to int, handle the case where it's missing, handle the case where it's not a number... for *each* flag. With argparse, it's three calls to `add_argument()`.

```bash
pytest -v -k "TestExtended"
git add -A && git commit -m "Lab 13: Add extended flags"
```

## Key Concepts

| Concept | What it means |
|---------|--------------|
| **`sys.argv`** | Raw list of command-line strings — no parsing, no validation |
| **`argparse`** | Standard library module for building command-line interfaces declaratively |
| **Positional argument** | Required argument identified by position (`wordcount.py report.txt`) |
| **Optional argument** | Flag identified by `--name` or `-n` (`--top 5`, `--ignore-case`) |
| **`choices`** | Restrict an argument to specific valid values |
| **`type`** | Automatic type conversion (string → int, etc.) |
| **`action="store_true"`** | Boolean flag — present means True, absent means False |

## Submission

Push your completed code and submit your repo URL.

Your commit history should look something like:
```
Lab 13: Organize project structure
Lab 13: Implement manual sys.argv word counter
Lab 13: Implement argparse word counter
Lab 13: Add extended flags
```

```bash
git push
```