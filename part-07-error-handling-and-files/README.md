# Part 07: Error Handling, Context Managers & File I/O

Robust software must anticipate errors and manage system resources (file descriptors, sockets, database transactions) cleanly. This module covers Python's exception handling mechanics, custom exception hierarchies, the `with` statement, custom context managers, and reading/writing structured data (Text, JSON, CSV).

---

## 📖 Key Topics

### 1. Exception Anatomy (`try-except-else-finally`)
```python
try:
    result = compute_risk_score(data)
except KeyError as err:
    # Handle missing dictionary key
    log_error(f"Missing field: {err}")
except ValueError as err:
    # Handle invalid numeric input
    log_error(f"Invalid value: {err}")
else:
    # Executes ONLY if NO exception was raised in 'try'
    persist_result(result)
finally:
    # ALWAYS executes, even if an exception or return occurred
    release_resources()
```

### 2. Custom Exceptions & Exception Chaining
- Subclass standard `Exception` (or a more specific built-in exception):
  ```python
  class ApplicationError(Exception):
      """Base exception for application errors."""

  class InsufficientInventoryError(ApplicationError):
      def __init__(self, item_id: str, requested: int, available: int):
          super().__init__(f"Item {item_id}: Requested {requested}, only {available} left.")
          self.item_id = item_id
  ```
- **Exception Chaining**: Use `raise ... from err` to preserve the original traceback for debugging.

### 3. Context Managers (`with` statement)
- Context managers guarantee that cleanup code runs even when errors occur.
- **Protocol**: An object implementing `__enter__()` and `__exit__(exc_type, exc_val, exc_tb)`.
- **Using `contextlib.contextmanager`**: Create a generator-based context manager with `yield`.

### 4. Modern File Operations with `pathlib`
- Prefer `pathlib.Path` over the legacy `os.path`.
- Always specify `encoding="utf-8"` when opening text files.
- Reading and writing:
  ```python
  from pathlib import Path
  path = Path("data.txt")
  path.write_text("Hello World", encoding="utf-8")
  content = path.read_text(encoding="utf-8")
  ```

### 5. Structured Data Formats (JSON & CSV)
- **JSON**: Serialization (`json.dumps`, `json.dump`) and deserialization (`json.loads`, `json.load`).
- **CSV**: Reading and writing tabular rows with `csv.DictReader` and `csv.DictWriter`.

---

## 🏃‍♂️ How to Run the Code

Run the accompanying script from your terminal:

```bash
python3 part-07-error-handling-and-files/main.py
```

---

## ✍️ Practice Exercises

1. **Config File Parser with Fallback**: Write a function that attempts to load settings from a JSON file. If the file is missing (`FileNotFoundError`) or invalid JSON (`json.JSONDecodeError`), log a warning and return default configuration settings.
2. **Benchmark Context Manager**: Create a custom context manager `@contextmanager` or class `Timer` that measures and prints elapsed time in milliseconds for any code block run inside a `with` block.
3. **CSV User Exporter**: Write a function that accepts a list of user dictionaries and exports them to a CSV file with columns `id`, `name`, `email`, and `signup_date`.
