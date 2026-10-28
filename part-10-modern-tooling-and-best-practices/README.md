# Part 10: Modern Tooling, Testing & Packaging

Writing functional Python code is only part of becoming a senior developer. Professional engineering requires automated testing, type checking, code styling, virtual environment isolation, and clean project architecture.

---

## 📖 Key Topics

### 1. Virtual Environments (`venv`)
Isolate project dependencies so different projects don't conflict:
```bash
# Create virtual environment
python3 -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

### 2. Modern Project Configuration (`pyproject.toml`)
- Replaces legacy `setup.py` and `setup.cfg` under PEP 518 and PEP 621.
- Centralizes build system settings, metadata, dependencies, and linter configurations (Ruff, Mypy, Pytest).

### 3. Automated Testing with `unittest` & `pytest`
- The standard library `unittest` module provides an xUnit-style framework:
  - Subclass `unittest.TestCase`.
  - Methods starting with `test_` are automatically discovered.
  - Lifecycle hooks: `setUp()` (runs before each test) and `tearDown()` (runs after each test).
  - Key assertions:
    - `self.assertEqual(a, b)`
    - `self.assertAlmostEqual(a, b, places=2)`
    - `self.assertRaises(ValueError)` (or `with self.assertRaises(...):`)
    - `self.assertTrue(x)`

### 4. Code Quality & Linting
- **Ruff**: Extremely fast Rust-based linter and formatter (replaces flake8, isort, and black).
- **Mypy**: Static type checker verifying PEP 484 annotations.
- **Pre-commit**: Git hooks that run linters automatically before code is committed.

---

## 🏃‍♂️ How to Run the Code & Tests

### Run the Application Script
```bash
python3 part-10-modern-tooling-and-best-practices/main.py
```

### Run the Unit Test Suite
```bash
python3 -m unittest part-10-modern-tooling-and-best-practices/test_calculator.py
```

---

## ✍️ Practice Exercises

1. **Extend Calculator**: Add `power(base, exponent)` and `square_root(n)` functions to `calculator.py`. Ensure `square_root` raises `ValueError` for negative inputs.
2. **Comprehensive Test Cases**: Write unit test cases for the newly added functions, checking edge cases (e.g. square root of 0, negative numbers, decimal exponents).
3. **Mocking External APIs**: Research `unittest.mock.patch` and write a test case simulating an external currency conversion API.
