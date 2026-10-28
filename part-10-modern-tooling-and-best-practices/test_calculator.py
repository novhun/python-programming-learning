"""
Unit Tests for Calculator Service
---------------------------------
Run using:
python3 -m unittest part-10-modern-tooling-and-best-practices/test_calculator.py
"""

import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        """Runs before every test method."""
        self.calc = Calculator()

    def tearDown(self) -> None:
        """Runs after every test method."""
        pass

    def test_addition(self) -> None:
        self.assertEqual(self.calc.add(10, 5), 15)
        self.assertEqual(self.calc.add(-3, -7), -10)
        self.assertAlmostEqual(self.calc.add(0.1, 0.2), 0.3, places=7)

    def test_subtraction(self) -> None:
        self.assertEqual(self.calc.subtract(10, 4), 6)
        self.assertEqual(self.calc.subtract(5, 10), -5)

    def test_multiplication(self) -> None:
        self.assertEqual(self.calc.multiply(6, 7), 42)
        self.assertEqual(self.calc.multiply(5, 0), 0)

    def test_division(self) -> None:
        self.assertEqual(self.calc.divide(20, 4), 5.0)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.3333333, places=6)

    def test_division_by_zero_raises(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_power(self) -> None:
        self.assertEqual(self.calc.power(2, 3), 8.0)
        self.assertEqual(self.calc.power(5, 0), 1.0)

    def test_square_root(self) -> None:
        self.assertEqual(self.calc.square_root(16), 4)
        self.assertAlmostEqual(self.calc.square_root(2), 1.41421356, places=5)

    def test_negative_square_root_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.square_root(-9)


if __name__ == "__main__":
    unittest.main()
