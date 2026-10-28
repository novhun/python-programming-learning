#!/usr/bin/env python3
"""
Part 07: Error Handling, Context Managers & File I/O
-----------------------------------------------------
This runnable script demonstrates:
1. Full try-except-else-finally flow
2. Custom exception classes and exception chaining (raise from)
3. Class-based Context Managers (__enter__ and __exit__)
4. Generator-based Context Managers (contextlib.contextmanager)
5. Modern File I/O using pathlib.Path (Text, JSON, and CSV)
"""

from __future__ import annotations
import contextlib
import csv
import json
from pathlib import Path
import time


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


# --- 1. Custom Exceptions ---
class CourseAppError(Exception):
    """Base exception for application errors."""


class InsufficientStockError(CourseAppError):
    """Raised when an inventory order exceeds stock."""

    def __init__(self, sku: str, requested: int, available: int) -> None:
        super().__init__(f"SKU '{sku}': Requested {requested} units, but only {available} in stock.")
        self.sku = sku
        self.requested = requested
        self.available = available


def process_order(sku: str, quantity: int, inventory: dict[str, int]) -> None:
    if sku not in inventory:
        raise KeyError(f"Product SKU '{sku}' not recognized.")
    available = inventory[sku]
    if quantity > available:
        raise InsufficientStockError(sku, quantity, available)
    inventory[sku] -= quantity
    print(f"  Order approved: {quantity}x {sku}. Remaining: {inventory[sku]}")


def demo_exception_handling() -> None:
    section("1. Exception Handling & Custom Exceptions")

    inventory = {"LAPTOP-01": 5, "MOUSE-02": 20}

    scenarios = [
        ("LAPTOP-01", 2),   # Success
        ("LAPTOP-01", 10),  # InsufficientStockError
        ("KEYBOARD-99", 1), # KeyError
    ]

    for sku, qty in scenarios:
        print(f"\nAttempting order: {qty}x {sku}")
        try:
            process_order(sku, qty, inventory)
        except InsufficientStockError as err:
            print(f"  [Handled Stock Error] {err}")
            print(f"    Details: SKU={err.sku}, Req={err.requested}, Avail={err.available}")
        except KeyError as err:
            print(f"  [Handled Catalog Error] Missing key: {err}")
        else:
            print("  [Else Clause] Transaction committed successfully to database.")
        finally:
            print("  [Finally Clause] Connection released back to pool.")


# --- 2. Custom Context Managers ---
class BenchmarkTimer:
    """Class-based context manager tracking execution time."""

    def __init__(self, label: str) -> None:
        self.label = label
        self.start_time: float = 0.0

    def __enter__(self) -> BenchmarkTimer:
        self.start_time = time.perf_counter()
        print(f"  [Timer '{self.label}'] Started.")
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> bool:
        elapsed = (time.perf_counter() - self.start_time) * 1000
        print(f"  [Timer '{self.label}'] Finished in {elapsed:.3f} ms.")
        # Returning False allows any exception to propagate normally
        return False


@contextlib.contextmanager
def temporary_status(target: dict[str, str], key: str, temp_value: str):
    """Generator-based context manager using contextlib."""
    old_value = target.get(key, "unassigned")
    target[key] = temp_value
    print(f"  [Context Entered] Set {key} = '{temp_value}'")
    try:
        yield target
    finally:
        target[key] = old_value
        print(f"  [Context Exited] Restored {key} = '{old_value}'")


def demo_context_managers() -> None:
    section("2. Custom Context Managers")

    # Using class-based timer
    with BenchmarkTimer("Heavy Math Loop"):
        total = sum(i * i for i in range(200_000))
        print(f"    Computed sum of squares: {total}")

    # Using generator-based context manager
    app_state = {"mode": "normal", "user": "guest"}
    print(f"\nBefore context: {app_state}")
    with temporary_status(app_state, "mode", "maintenance") as state:
        print(f"    Inside context block: current state = {state}")
    print(f"After context:  {app_state}")


# --- 3. File I/O with pathlib, JSON, and CSV ---
def demo_file_operations() -> None:
    section("3. File Operations (pathlib, JSON, CSV)")

    sandbox_dir = Path(__file__).parent / "sandbox"
    sandbox_dir.mkdir(exist_ok=True)
    print(f"Sandbox directory ready: {sandbox_dir}")

    # 1. Plain Text File
    text_file = sandbox_dir / "sample_log.txt"
    text_file.write_text("2026-10-28 INFO: Application booted successfully.\n", encoding="utf-8")
    with text_file.open("a", encoding="utf-8") as f:
        f.write("2026-10-28 INFO: Health check passed.\n")

    print(f"\nRead Text File ({text_file.name}):")
    print(text_file.read_text(encoding="utf-8").strip())

    # 2. JSON Serialization
    json_file = sandbox_dir / "course_config.json"
    data = {
        "course_title": "Python Programming Mastery",
        "version": "2.0.0",
        "modules_count": 10,
        "is_published": True,
        "tags": ["python", "oop", "asyncio", "testing"],
    }
    with json_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with json_file.open("r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    print(f"\nParsed JSON from {json_file.name}:")
    print(f"  Title: {loaded_data['course_title']}, Tags: {loaded_data['tags']}")

    # 3. CSV File (DictWriter and DictReader)
    csv_file = sandbox_dir / "students.csv"
    students = [
        {"id": "S101", "name": "Maya Lin", "grade": "A"},
        {"id": "S102", "name": "Liam Chen", "grade": "B+"},
        {"id": "S103", "name": "Sofia Rossi", "grade": "A+"},
    ]

    # Write CSV
    with csv_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "grade"])
        writer.writeheader()
        writer.writerows(students)

    # Read CSV
    print(f"\nRead CSV from {csv_file.name}:")
    with csv_file.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"  ID: {row['id']:<5} | Name: {row['name']:<12} | Grade: {row['grade']}")


def main() -> None:
    print("╔═══════════════════════════════════════════════╗")
    print("║     Part 07: Error Handling & File I/O        ║")
    print("╚═══════════════════════════════════════════════╝")

    demo_exception_handling()
    demo_context_managers()
    demo_file_operations()

    print("\n✅ Part 07 execution complete!")


if __name__ == "__main__":
    main()
