# Part 03: Data Structures Mastery

Python's built-in collections—**Lists, Tuples, Dictionaries, and Sets**—are the workhorses of almost every Python application. Understanding their performance characteristics, mutability, and syntax idioms is essential for writing fast and maintainable code.

---

## 📖 Key Topics

### 1. Lists (Mutable, Ordered)
- Indexing & Slicing: `sequence[start:stop:step]`
  - Negative indexing: `seq[-1]` is the last element.
  - Reversing a list with slice: `seq[::-1]`.
- Key Methods:
  - `.append(x)`: Adds item to the end (amortized $O(1)$).
  - `.extend(iterable)`: Appends elements from an iterable.
  - `.insert(i, x)`: Inserts element at index $i$ ($O(n)$).
  - `.pop([i])`: Removes and returns item at index $i$ (default last element).
  - `.sort(key=..., reverse=...)`: In-place Timsort ($O(n \log n)$).

### 2. Tuples (Immutable, Ordered)
- Defined with parentheses: `t = (1, 2, 3)`. Note: a single-element tuple needs a trailing comma: `(42,)`.
- **Tuple Unpacking**:
  ```python
  x, y, *rest = [1, 2, 3, 4, 5]  # x=1, y=2, rest=[3, 4, 5]
  ```
- Because tuples are immutable, they are hashable (if their elements are hashable) and can be used as dictionary keys or set items.

### 3. Dictionaries (Key-Value, Mutable, Preserves Insertion Order)
- Keys must be **hashable** (immutable types like strings, numbers, tuples).
- Average $O(1)$ lookup, insertion, and deletion.
- Safe retrieval:
  - `d.get(key, default_value)` prevents `KeyError`.
  - `d.setdefault(key, default)` returns the value if present, else sets it to default.
- Dictionary unpacking / merging:
  ```python
  merged = {**dict_a, **dict_b}
  # Or Python 3.9+ union operator:
  merged = dict_a | dict_b
  ```

### 4. Sets (Unique Elements, Mutable, Unordered)
- Highly efficient membership testing: `x in my_set` ($O(1)$ average).
- Mathematical Set Operations:
  - **Union** (`A | B`): Elements in A, B, or both.
  - **Intersection** (`A & B`): Elements in both A and B.
  - **Difference** (`A - B`): Elements in A but not in B.
  - **Symmetric Difference** (`A ^ B`): Elements in A or B, but not both.

### 5. Comprehensions
Expressive, readable, and often faster than traditional loops:
```python
# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
square_map = {x: x**2 for x in range(5)}

# Set comprehension
unique_lengths = {len(word) for word in ["apple", "banana", "pear", "apple"]}
```

### 6. Mutability & Copying (`copy` module)
- Simple assignment `b = a` copies the **pointer/reference**, not the object.
- `copy.copy(x)`: Shallow copy (creates new outer container, but shares nested mutable objects).
- `copy.deepcopy(x)`: Deep copy (recursively duplicates all nested objects).

---

## 🏃‍♂️ How to Run the Code

Run the accompanying script from your terminal:

```bash
python3 part-03-data-structures/main.py
```

---

## ✍️ Practice Exercises

1. **Word Frequency Counter**: Given a long sentence, return a dictionary where keys are unique lowercase words and values are their occurrence counts (without using external libraries).
2. **Duplicate Remover**: Given a list with duplicates, preserve the original order of first occurrences while removing all duplicates.
3. **Inventory Management**: Write a function that merges two stock dictionaries, adding together quantities for items present in both inventories.
