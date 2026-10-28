# Part 02: Control Flow & Loops

Mastering control flow allows your programs to make decisions, branch logic, and repeat tasks efficiently. This module explores conditional logic, modern pattern matching (`match-case`), loops, loop control statements, and idiomatic Python iteration helpers.

---

## 📖 Key Topics

### 1. Conditionals & Logical Operators
- Basic syntax:
  ```python
  if score >= 90:
      grade = "A"
  elif score >= 80:
      grade = "B"
  else:
      grade = "C"
  ```
- **Ternary Operator** (Inline conditional expression):
  ```python
  status = "Adult" if age >= 18 else "Minor"
  ```
- **Logical Operators & Short-circuiting**:
  - `and`: Evaluates to `False` immediately if the left operand is falsy.
  - `or`: Evaluates to `True` immediately if the left operand is truthy.
  - `not`: Inverts boolean value.

### 2. Identity vs Equality (`is` vs `==`)
- `==` checks **value equality** (do they have the same contents?).
- `is` checks **object identity** (do they reference the exact same memory address?).
- Always use `is None` and `is not None` when checking for `None`.

### 3. Structural Pattern Matching (`match-case`)
Introduced in Python 3.10, `match-case` is much more powerful than traditional `switch` statements:
```python
match command.split():
    case ["quit"]:
        print("Exiting...")
    case ["load", filename]:
        print(f"Loading {filename}")
    case ["save", filename] if filename.endswith(".json"):
        print(f"Saving JSON to {filename}")
    case _:
        print("Unknown command")
```

### 4. Loops & Loop Controls
- `while <condition>`: Loops while a boolean condition remains `True`.
- `for <item> in <iterable>`: Loops through items in a collection or generator.
- `break`: Immediately exits the loop.
- `continue`: Skips the rest of the current iteration and jumps to the next.
- **The Loop `else` clause**:
  - A `for-else` or `while-else` executes **only** if the loop completes without encountering a `break`.
  - Excellent for search algorithms (e.g., "item not found" logic without extra boolean flags).

### 5. Idiomatic Iteration Utilities
- `range(start, stop, step)`: Generates numbers on demand.
- `enumerate(iterable, start=0)`: Yields pairs of `(index, item)`.
- `zip(seq1, seq2)`: Pairs elements from multiple sequences together.
- `reversed(seq)`: Iterates backwards without mutating the original sequence.

---

## 🏃‍♂️ How to Run the Code

Run the accompanying script from your terminal:

```bash
python3 part-02-control-flow-and-loops/main.py
```

---

## ✍️ Practice Exercises

1. **Prime Number Finder**: Write a loop using `for-else` that checks whether a given number $N$ is prime, breaking when a factor is found and using `else` to declare it prime.
2. **FizzBuzz**: For numbers from 1 to 50:
   - Print "Fizz" if divisible by 3.
   - Print "Buzz" if divisible by 5.
   - Print "FizzBuzz" if divisible by both.
   - Otherwise, print the number.
3. **HTTP Status Code Matcher**: Using `match-case`, write a function that takes an HTTP status code (e.g., 200, 404, 500) and prints its classification and descriptive message.
