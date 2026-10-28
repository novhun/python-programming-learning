# Part 06: Advanced OOP & Architecture

Building upon foundational OOP, this module explores enterprise architectural patterns in Python: inheritance hierarchies, multiple inheritance, Method Resolution Order (MRO), abstract contracts (`abc`), polymorphism, composition, and modern `@dataclass` models.

---

## 📖 Key Topics

### 1. Inheritance & `super()`
- Subclasses inherit attributes and methods from base classes.
- Overriding methods allows specialized behavior.
- `super().__init__(...)` delegates initialization cleanly to parent classes.

### 2. Multiple Inheritance & Method Resolution Order (MRO)
- Python supports multiple inheritance: `class C(A, B):`.
- Resolving which method to call is governed by the **C3 Linearization Algorithm** (Method Resolution Order).
- Inspect the resolution order using `ClassName.mro()` or `ClassName.__mro__`.
- Solves the classic "Diamond Problem" deterministically.

### 3. Abstract Base Classes (ABCs)
- In Python, interfaces and contracts are defined using `abc.ABC` and the `@abstractmethod` decorator.
- Any subclass that does not implement all abstract methods cannot be instantiated (raises `TypeError`).

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Process the transaction."""
```

### 4. Polymorphism & Duck Typing
- *"If it walks like a duck and quacks like a duck, it's a duck."*
- Python functions do not care about an object's strict type as long as it provides the requested interface or methods.

### 5. Composition Over Inheritance
- Inheritance models an **"is-a"** relationship (e.g., `Dog` *is an* `Animal`).
- Composition models a **"has-a"** relationship (e.g., `Car` *has an* `Engine`).
- Composition produces less rigid, more easily testable architectures.

### 6. Modern Dataclasses (`@dataclass`)
- Introduced in Python 3.7 to eliminate boilerplate:
  ```python
  from dataclasses import dataclass, field

  @dataclass(frozen=True)
  class UserConfig:
      username: str
      email: str
      roles: list[str] = field(default_factory=list)
  ```
- Automatically generates `__init__`, `__repr__`, `__eq__`, and hashing (when `frozen=True`).

---

## 🏃‍♂️ How to Run the Code

Run the accompanying script from your terminal:

```bash
python3 part-06-oop-advanced/main.py
```

---

## ✍️ Practice Exercises

1. **Notification System**: Create an abstract base class `NotificationService(ABC)` with abstract method `send(recipient, message)`. Implement `EmailNotification`, `SMSNotification`, and `SlackNotification` classes. Use polymorphism to dispatch a message to a list of services.
2. **Diamond Problem Investigation**: Create classes `Device`, `Phone(Device)`, `Computer(Device)`, and `Smartphone(Phone, Computer)`. Inspect and explain `Smartphone.mro()`.
3. **Immutable Configuration Dataclass**: Create a `@dataclass(frozen=True)` representing database connection settings (`host`, `port`, `database`, `ssl`). Test that modifying any attribute raises a `FrozenInstanceError`.
