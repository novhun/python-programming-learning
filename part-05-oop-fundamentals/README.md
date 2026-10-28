# Part 05: Object-Oriented Programming (OOP) Fundamentals

Object-Oriented Programming (OOP) is a paradigm centered around objects containing both state (attributes) and behavior (methods). In Python, almost everything is an object. Mastering OOP fundamentals helps you model complex domains cleanly.

---

## 📖 Key Topics

### 1. Classes, Objects & `self`
- A **class** is a blueprint; an **object** (or instance) is a concrete realization created from that blueprint.
- `__init__(self, ...)` is the initializer called when a new instance is created.
- `self` explicitly represents the instance itself and must be the first parameter of any instance method.

```python
class BankAccount:
    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        self.account_holder = account_holder
        self.balance = initial_balance
```

### 2. Instance vs Class Attributes
- **Instance Attributes**: Bound to `self`. Each instance has its own separate copy.
- **Class Attributes**: Defined directly inside the class body. Shared across all instances of that class.

### 3. Instance, Class, and Static Methods
| Method Type | Decorator | First Parameter | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **Instance Method** | None | `self` | Access or modify instance state |
| **Class Method** | `@classmethod` | `cls` | Factory methods / Alternative constructors, modifying class state |
| **Static Method** | `@staticmethod` | None | Pure utility functions belonging logically to the class namespace |

### 4. Encapsulation & Properties
- Python uses naming conventions for access control:
  - `public_var`: Accessible anywhere.
  - `_protected_var`: Internal convention; hints that callers shouldn't touch it directly.
  - `__private_var`: Name mangling (renamed to `_ClassName__private_var` to prevent accidental override).
- **The `@property` Decorator**:
  - Turns a method into an attribute getter with optional setter validation.

```python
class Employee:
    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value
```

### 5. Dunder (Magic) Methods
Special methods starting and ending with double underscores:
- `__str__(self)`: Human-readable string for `print()` and end users.
- `__repr__(self)`: Unambiguous representation, ideal for debugging (`f"{self.__class__.__name__}(...)"`).
- `__len__(self)`: Implements `len(obj)`.
- `__eq__(self, other)`: Implements `==`.
- `__add__(self, other)`: Implements `+`.

---

## 🏃‍♂️ How to Run the Code

Run the accompanying script from your terminal:

```bash
python3 part-05-oop-fundamentals/main.py
```

---

## ✍️ Practice Exercises

1. **Shopping Cart Item**: Create an `Item` class with `name`, `price`, and `quantity`. Implement `@property` for `total_price` ($price \times quantity$), with validation preventing negative price or quantity.
2. **Alternative Constructor**: Add a `@classmethod` `from_csv_string(cls, line)` to `Item` that parses `"Keyboard,49.99,2"` into an `Item` instance.
3. **Money Class**: Create a `Money(amount, currency)` class that overrides `__add__` to allow adding two `Money` instances of the same currency (raising a `ValueError` if currencies do not match), and implements `__repr__` and `__eq__`.
