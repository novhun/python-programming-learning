#!/usr/bin/env python3
"""
Part 03: Data Structures Mastery
----------------------------------
This runnable script demonstrates:
1. Lists: Slicing, manipulation, in-place sorting with custom keys
2. Tuples & Extended Unpacking
3. Dictionaries: Access patterns, defaults, and modern merge syntax
4. Sets & Set Algebra (Union, Intersection, Difference)
5. List, Dictionary, and Set Comprehensions
6. Shallow Copy vs Deep Copy pitfalls
7. Bonus: collections.defaultdict and collections.Counter
"""

import copy
from collections import Counter, defaultdict


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def demo_lists() -> None:
    section("1. Lists: Slicing & Custom Sorting")

    numbers = [10, 25, 30, 45, 50, 65, 70, 85, 90]
    print(f"Original numbers: {numbers}")

    # Slicing syntax: [start:stop:step]
    print(f"  First 3 items ([:3]):          {numbers[:3]}")
    print(f"  Last 3 items ([-3:]):          {numbers[-3:]}")
    print(f"  Every 2nd item ([::2]):        {numbers[::2]}")
    print(f"  Reversed slice ([::-1]):       {numbers[::-1]}")

    # Complex sorting with lambda key
    employees = [
        {"name": "Diana", "department": "Eng", "salary": 115000},
        {"name": "Bob", "department": "Design", "salary": 95000},
        {"name": "Charlie", "department": "Eng", "salary": 130000},
        {"name": "Alice", "department": "HR", "salary": 80000},
    ]

    # Sort in-place by salary descending
    employees.sort(key=lambda emp: emp["salary"], reverse=True)
    print("\nEmployees sorted by Salary (Descending):")
    for emp in employees:
        print(f"  {emp['name']:<10} | {emp['department']:<8} | ${emp['salary']:,}")


def demo_tuples_and_unpacking() -> None:
    section("2. Tuples & Extended Unpacking")

    # Creating tuples
    single_item = (42,)  # Notice the trailing comma
    point_3d = (10, 20, 30)
    print(f"Single item tuple: {single_item} (type: {type(single_item).__name__})")
    print(f"3D Point: {point_3d}")

    # Extended unpacking with starred expression
    record = ("server-prod-01", "192.168.1.100", "22", "80", "443", "8080")
    server_name, ip_address, *ports = record

    print("\nUnpacking Server Record:")
    print(f"  Server Name: {server_name}")
    print(f"  IP Address:  {ip_address}")
    print(f"  Open Ports:  {ports} (Extracted as list: {len(ports)} ports)")


def demo_dictionaries() -> None:
    section("3. Dictionaries & Modern Merge")

    user_profile = {
        "id": 1042,
        "username": "codemaster",
        "email": "code@example.com",
    }

    # Safe retrieval with get and setdefault
    role = user_profile.get("role", "Guest")
    print(f"User role (safe get with default): {role}")

    # setdefault adds the key if it doesn't exist
    tags = user_profile.setdefault("tags", ["python", "developer"])
    print(f"Tags after setdefault: {tags}")
    print(f"Profile updated: {user_profile}")

    # Merging dictionaries (Python 3.9+ union operator |)
    defaults = {"theme": "dark", "notifications": True, "language": "en"}
    custom_prefs = {"theme": "solarized", "language": "es"}
    final_settings = defaults | custom_prefs

    print(f"\nDefault settings:  {defaults}")
    print(f"Custom overrides:  {custom_prefs}")
    print(f"Merged settings:   {final_settings}")


def demo_sets_and_algebra() -> None:
    section("4. Sets & Set Algebra")

    frontend_devs = {"Alice", "Bob", "Charlie", "David"}
    backend_devs = {"Charlie", "David", "Eve", "Frank"}

    print(f"Frontend Team: {frontend_devs}")
    print(f"Backend Team:  {backend_devs}")

    # Set operations
    full_stack = frontend_devs & backend_devs  # Intersection
    all_engineers = frontend_devs | backend_devs  # Union
    frontend_only = frontend_devs - backend_devs  # Difference
    single_discipline = frontend_devs ^ backend_devs  # Symmetric Difference

    print(f"\n  Full-Stack (Both Teams):        {full_stack}")
    print(f"  All Engineers (Union):          {all_engineers}")
    print(f"  Frontend Only:                  {frontend_only}")
    print(f"  Single Discipline (Either/Not Both): {single_discipline}")


def demo_comprehensions() -> None:
    section("5. Comprehensions (List, Dict, Set)")

    numbers = range(1, 11)

    # List comprehension with filtering
    even_squares = [n**2 for n in numbers if n % 2 == 0]
    print(f"Even squares (List): {even_squares}")

    # Dict comprehension: mapping number to its cube
    cubes_map = {n: n**3 for n in range(1, 6)}
    print(f"Number to Cube (Dict): {cubes_map}")

    # Set comprehension: collecting unique word lengths
    sentence = "the quick brown fox jumps over the lazy dog"
    word_lengths = {len(word) for word in sentence.split()}
    print(f"Unique word lengths (Set): {sorted(word_lengths)}")


def demo_copying_pitfalls() -> None:
    section("6. Mutability: Shallow vs Deep Copy")

    original = [["apple", "banana"], [1, 2, 3]]

    shallow = copy.copy(original)
    deep = copy.deepcopy(original)

    # Mutating nested list in original
    original[0].append("cherry")

    print("After appending 'cherry' to original[0]:")
    print(f"  Original: {original}")
    print(f"  Shallow:  {shallow}  <-- Notice: Shallow copy WAS modified!")
    print(f"  Deep:     {deep}     <-- Notice: Deep copy remained isolated!")


def demo_collections_bonus() -> None:
    section("7. Bonus: collections.defaultdict & Counter")

    text = "apple banana apple cherry banana apple date"
    word_counts = Counter(text.split())
    print(f"Word frequency with Counter: {dict(word_counts)}")
    print(f"Top 2 most common: {word_counts.most_common(2)}")

    # Grouping with defaultdict
    cities_by_country = defaultdict(list)
    cities_by_country["Japan"].append("Tokyo")
    cities_by_country["Japan"].append("Kyoto")
    cities_by_country["Canada"].append("Toronto")

    print(f"Grouped with defaultdict: {dict(cities_by_country)}")


def main() -> None:
    print("╔═══════════════════════════════════════════════╗")
    print("║     Part 03: Data Structures Mastery          ║")
    print("╚═══════════════════════════════════════════════╝")

    demo_lists()
    demo_tuples_and_unpacking()
    demo_dictionaries()
    demo_sets_and_algebra()
    demo_comprehensions()
    demo_copying_pitfalls()
    demo_collections_bonus()

    print("\n✅ Part 03 execution complete!")


if __name__ == "__main__":
    main()
