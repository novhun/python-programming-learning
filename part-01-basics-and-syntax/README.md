# Part 01: Python Basics & Syntax

Welcome to the foundation of Python programming. In this module, you will learn the fundamental building blocks of Python, how variables and data types behave in Python's dynamic type system, operators, string formatting, and user input/output.

---

## 📖 Key Topics

### 1. Variables & Dynamic Typing
- Python is **dynamically typed**: you do not declare variable types explicitly; Python infers types at runtime.
- Variable names follow **PEP 8 style guide** (`snake_case` for variables and functions, UPPERCASE for constants).
- Reassigning a variable can change its type freely.

```python
age = 25              # int
pi = 3.14159          # float
name = "Alice"        # str
is_student = True     # bool
salary = None         # NoneType
```

### 2. Type Checking & Casting
- `type(x)` returns the type of variable `x`.
- `isinstance(x, int)` returns `True` if `x` is an instance of `int` (or a subclass).
- Casting functions:
  - `int("42")` -> `42`
  - `float("3.14")` -> `3.14`
  - `str(100)` -> `"100"`
  - `bool(0)` -> `False` (Truthy/Falsy conversion)

### 3. Arithmetic Operators
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- True Division: `/` (always returns a `float`, e.g., `7 / 2 = 3.5`)
- Floor Division: `//` (integer division, e.g., `7 // 2 = 3`)
- Modulo: `%` (remainder, e.g., `7 % 2 = 1`)
- Exponentiation: `**` (e.g., `2 ** 3 = 8`)

### 4. String Manipulation & F-Strings
- Modern formatted strings (F-strings introduced in Python 3.6):
  ```python
  item = "Laptop"
  price = 1299.9876
  print(f"{item} costs ${price:.2f}")  # Laptop costs $1300.00
  ```
- Common string methods:
  - `.strip()`: Removes leading and trailing whitespace
  - `.upper()`, `.lower()`, `.title()`: Case transformations
  - `.replace(old, new)`: Replace occurrences
  - `.split(delimiter)`: Split into a list of strings
  - `delimiter.join(list)`: Combine a list into a string

### 5. Input and Output
- `print(*objects, sep=' ', end='\n')`: Custom separators and endings.
- `input(prompt)`: Reads a line from console as a `str` (always cast if numeric input is needed).

---

## 🏃‍♂️ How to Run the Code

Run the accompanying script from your terminal:

```bash
python3 part-01-basics-and-syntax/main.py
```

---

## ✍️ Practice Exercises

1. **Temperature Converter**: Write a function that takes a temperature in Celsius (float) and converts it to Fahrenheit ($F = C \times \frac{9}{5} + 32$) formatted to 1 decimal place.
2. **Tip Calculator**: Given a bill amount and tip percentage, calculate the tip and total amount, formatted as currency (`$XX.XX`).
3. **Initials Extractor**: Given a user's full name (e.g., `"guido van rossum"`), extract and print their uppercase initials (e.g., `"G.V.R."`).
