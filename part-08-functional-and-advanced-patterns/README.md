# Part 08: Functional & Advanced Python Patterns

This module dives into the advanced Python patterns used by senior engineers and library authors: the iterator protocol, memory-efficient generators, composable generator pipelines, custom decorators, and powerful standard library tools (`functools` and `itertools`).

---

## 📖 Key Topics

### 1. The Iterator Protocol
- **Iterable**: An object capable of returning members one at a time (implements `__iter__()`).
- **Iterator**: An object representing a stream of data; successive calls to `__next__()` yield items until `StopIteration` is raised.

### 2. Generators & `yield`
- Functions containing the `yield` keyword return a generator object without running the entire function upfront.
- Execution pauses at each `yield` and resumes on the next request.
- **Memory Efficiency**: Can process billions of rows or infinite streams with minimal RAM usage.
- **Generator Expressions**:
  ```python
  squares_gen = (x**2 for x in range(1_000_000))  # Takes almost 0 bytes of RAM
  ```

### 3. Decorators
A decorator is a callable that accepts a function as an argument and returns a replacement function, wrapping or altering behavior.
- Always use `@functools.wraps(func)` to preserve function name, docstring, and annotations.
- **Decorator with Arguments**:
  Requires 3 levels of nesting:
  ```python
  def repeat(num_times: int):
      def decorator(func):
          @functools.wraps(func)
          def wrapper(*args, **kwargs):
              for _ in range(num_times):
                  result = func(*args, **kwargs)
              return result
          return wrapper
      return decorator
  ```

### 4. `functools` Utilities
- `@lru_cache(maxsize=128)`: Automatic memoization/caching for pure functions (e.g. recursive algorithms, API queries).
- `partial(func, *args, **kwargs)`: Pre-fills function arguments to create specialized functions.

### 5. `itertools` Utilities
- `itertools.chain(*iterables)`: Chains multiple iterables sequentially.
- `itertools.islice(iterable, start, stop)`: Slices an iterator lazily without converting to a list.
- `itertools.cycle(iterable)`: Cycles infinitely over a sequence.

---

## 🏃‍♂️ How to Run the Code

Run the accompanying script from your terminal:

```bash
python3 part-08-functional-and-advanced-patterns/main.py
```

---

## ✍️ Practice Exercises

1. **Fibonacci Generator**: Write a generator `fibonacci()` that yields an infinite sequence of Fibonacci numbers ($0, 1, 1, 2, 3, 5, \dots$). Use `itertools.islice` to extract the first 20 numbers.
2. **Retry Decorator**: Write a decorator `@retry(max_retries=3, delay_seconds=0.1)` that catches exceptions and retries the function up to `max_retries` before re-raising the error.
3. **Log Execution Decorator**: Write a decorator `@log_execution` that logs function name, input arguments, and return value before and after each call.
