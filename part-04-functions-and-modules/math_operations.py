"""
Math Operations Helper Module
-----------------------------
Demonstrates:
- Proper module docstrings
- Function type annotations
- The __all__ export whitelist
- The __name__ == '__main__' self-test pattern
"""

from __future__ import annotations
import math

__all__ = ["calculate_mean", "calculate_median", "factorial", "is_even"]


def calculate_mean(numbers: list[float]) -> float:
    """Calculate the arithmetic mean of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate mean of an empty list.")
    return sum(numbers) / len(numbers)


def calculate_median(numbers: list[float]) -> float:
    """Calculate the median of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate median of an empty list.")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 1:
        return sorted_nums[mid]
    return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0


def factorial(n: int) -> int:
    """Compute n factorial using math.prod or recursion."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers.")
    return math.prod(range(1, n + 1)) if n > 0 else 1


def is_even(n: int) -> bool:
    """Check if an integer is even."""
    return n % 2 == 0


if __name__ == "__main__":
    print("[math_operations.py] Self-test running directly:")
    test_data = [10.0, 20.0, 30.0, 40.0, 50.0]
    print(f"  Test data: {test_data}")
    print(f"  Mean:      {calculate_mean(test_data)}")
    print(f"  Median:    {calculate_median(test_data)}")
    print(f"  5! =       {factorial(5)}")
