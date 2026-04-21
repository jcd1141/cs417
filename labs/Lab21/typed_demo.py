def greet(name: str) -> str:
    return f"Hello, {name}!"

def square(n: int) -> int:
    return n * n

def is_adult(age: int) -> bool:
    return age >= 18

def total_grades(grades: list[int]) -> int:
    return sum(grades)

def grade_lookup(roster: dict[str, int], name: str) -> int:
    return roster[name]

def first_and_last(items: list[str]) -> tuple[str, str]:
    return items[0], items[-1]

from typing import TypedDict

class StudentRow(TypedDict):
    name: str
    email: str
    grade: str

def read_roster(path: str) -> list[StudentRow]:
    # pretend this reads a CSV
    return [{"name": "Alice", "email": "alice@uni.edu", "grade": "92"}]
