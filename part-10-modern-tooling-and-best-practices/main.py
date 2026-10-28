#!/usr/bin/env python3
"""
Part 10: Modern Tooling, Testing & Packaging
---------------------------------------------
This runnable script demonstrates:
1. Clean service design with the Calculator class
2. Programmatically invoking the unittest test suite and displaying results
3. Modern Python project configuration (pyproject.toml, virtual environments, Ruff, Mypy)
"""

from __future__ import annotations
import sys
import unittest
from calculator import Calculator
from test_calculator import TestCalculator


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def demo_calculator_service() -> None:
    section("1. Calculator Service Execution")

    calc = Calculator()
    print("Executing operations:")
    print(f"  Addition:       12.5 + 7.5  = {calc.add(12.5, 7.5)}")
    print(f"  Subtraction:    100 - 35    = {calc.subtract(100, 35)}")
    print(f"  Multiplication: 8 * 9       = {calc.multiply(8, 9)}")
    print(f"  Division:       150 / 6     = {calc.divide(150, 6)}")
    print(f"  Power:          2 ** 10     = {calc.power(2, 10)}")
    print(f"  Square Root:    sqrt(144)   = {calc.square_root(144)}")

    try:
        calc.divide(50, 0)
    except ZeroDivisionError as err:
        print(f"  Handled division by zero: {err}")


def run_unit_tests() -> None:
    section("2. Executing Automated Test Suite (unittest)")

    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    runner = unittest.TextTestRunner(verbosity=2)
    print("Running test suite dynamically...\n")
    result = runner.run(suite)

    print(f"\nTests run: {result.testsRun}")
    print(f"Failures:  {len(result.failures)}")
    print(f"Errors:    {len(result.errors)}")
    if result.wasSuccessful():
        print("🎉 ALL UNIT TESTS PASSED!")


def demo_best_practices_summary() -> None:
    section("3. Production Best Practices Checklist")

    checklist = [
        ("Virtual Environment", "Use 'python3 -m venv .venv' for dependency isolation"),
        ("Modern Packaging", "Use pyproject.toml (PEP 518/621) instead of legacy setup.py"),
        ("Linting & Formatting", "Use Ruff for lightning-fast linting and automatic formatting"),
        ("Type Checking", "Use mypy for strict static type validation"),
        ("Automated Tests", "Write unit tests for edge cases with unittest or pytest"),
        ("Continuous Integration", "Run linting, type checks, and tests on every Git push (GitHub Actions)"),
    ]

    for title, desc in checklist:
        print(f"  ✔ {title:<22} : {desc}")


def main() -> None:
    print("╔═══════════════════════════════════════════════╗")
    print("║     Part 10: Modern Tooling & Testing         ║")
    print("╚═══════════════════════════════════════════════╝")

    demo_calculator_service()
    run_unit_tests()
    demo_best_practices_summary()

    print("\n✅ Part 10 execution complete!")


if __name__ == "__main__":
    main()
