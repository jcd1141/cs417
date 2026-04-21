1. The section that showed me a bug was the optional one. Mypy said something like you can’t add int and None. The mistake was adding 10 to something that might be None. That’s easy to miss in Python because it looks fine until it actually runs and crashes.

2. There’s no runtime cost because Python ignores type hints. The benefit is catching bugs before running the code. If Python enforced types like Java, it would probably catch more errors automatically but make the language less flexible and slower.

3. I would use TypedDict when the dict always has the same keys, like a student row. I would use dict[K, V] when the keys can change, like mapping IDs to values. TypedDict helps catch key mistakes, plain dict is better for general use. The lab explains this.