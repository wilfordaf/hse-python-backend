import math
from typing import List, TypeVar


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Number must be non-negative")

    return math.factorial(n)


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Number must be non-negative")

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    return a


T = TypeVar("T", int, float)


def mean(numbers: List[T]) -> float:
    if not numbers:
        raise ValueError("Array cannot be empty")

    return sum(numbers) / len(numbers)
