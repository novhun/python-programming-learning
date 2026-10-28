# Part 04: Functions, Scopes & Modules

Functions are the core unit of modularity and code reuse in Python. In this module, you will master parameter passing, modern type annotations, the LEGB scope hierarchy, closures, lambda expressions, and modular code organization.

---

## 📖 Key Topics

### 1. Function Signatures & Arguments
- **Positional vs Keyword Arguments**: Parameters can be passed by position or explicitly by name.
- **Positional-Only (`/`) & Keyword-Only (`*`) Markers**:
  ```python
  def configure(server: str, /, timeout: int = 30, *, debug: bool = False):
      # 'server' MUST be positional
      # 'timeout' can be positional or keyword
      # 'debug' MUST be passed as a keyword argument (e.g., debug=True)
      pass
  ```
- **Arbitrary Arguments**:
  - `*args`: Collects extra positional arguments as a `tuple`.
  - `**kwargs`: Collects extra keyword arguments as a `dict`.
- **The Mutable Default Argument Trap**:
  - Never use a mutable object (like `[]` or `{}`) as a default argument.
  - The default object is created once when the function is defined, sharing state across invocations.
  - Idiomatic fix:
    ```python
    def append_item(item, target=None):
        if target is None:
            target = []
        target.append(item)
        return target
    ```

### 2. Type Hints (PEP 484 & Modern Python)
- Clean, readable annotations for static analysis and IDE autocompletion:
  ```python
  def calculate_stats(scores: list[float]) -> dict[str, float]:
      return {"min": min(scores), "max": max(scores), "avg": sum(scores) / len(scores)}
  ```

### 3. Scope & The LEGB Rule
Python resolves variable names in this order:
1. **L**ocal: Defined inside the current function.
2. **E**nclosing: Defined inside any enclosing functions (closures).
3. **G**lobal: Defined at the module top level.
4. **B**uilt-in: Built-in Python functions and keywords (`print`, `len`, `int`).
- Modifying outer scopes requires `global` (module level) or `nonlocal` (enclosing function level).

### 4. Lambdas & Higher-Order Functions
- Anonymous inline functions: `lambda x, y: x + y`
- Functions as first-class citizens: can be passed into functions or returned from functions.
- `map(func, iterable)`, `filter(predicate, iterable)`, `functools.reduce(func, iterable)`.

### 5. Modules, Packages & `__name__`
- Organizing code across multiple `.py` files.
- `__all__ = [...]` controls what gets exported with `from module import *`.
- The `if __name__ == "__main__":` idiom ensures code runs when invoked as a script, but not when imported.

---

## 🏃‍♂️ How to Run the Code

Run the accompanying script from your terminal:

```bash
python3 part-04-functions-and-modules/main.py
```

---

## ✍️ Practice Exercises

1. **Flexible Logger**: Write a function `log_message(level, *messages, timestamp=True, **metadata)` that formats and prints logging messages with optional timestamp and key-value metadata tags.
2. **Stateful Counter Closure**: Write a function `make_counter(start=0, step=1)` that returns a closure function. Each time the closure is called, it increments by `step` and returns the new value (use `nonlocal`).
3. **Data Pipeline**: Using `map`, `filter`, and `lambda`, take a list of raw transaction amounts, filter out negative/fraudulent numbers, apply a 7% sales tax to each, and calculate the total.
