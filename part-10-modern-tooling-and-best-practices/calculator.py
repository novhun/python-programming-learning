"""
Production Calculator Service
-----------------------------
Demonstrates clean design, type annotations, and validation
for automated unit testing.
"""

from __future__ import annotations
import math


class Calculator:
    """Scientific calculator service."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        return math.pow(base, exponent)

    def square_root(self, n: float) -> float:
        if n < 0:
            raise ValueError("Square root is not defined for negative real numbers.")
        return math.isqrt(int(n)) if n.is_integer() and n >= 0 and math.isqrt(int(n)) ** 2 == int(n) else math.sqrt(n)
