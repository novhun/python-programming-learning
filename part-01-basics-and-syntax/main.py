#!/usr/bin/env python3
"""
Part 01: Python Basics & Syntax
---------------------------------
This runnable script demonstrates:
1. Dynamic typing and basic data types
2. Type checking and casting
3. Arithmetic operators
4. String methods and modern f-string formatting
5. Print formatting (sep, end) and simulated input handling
"""


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def demo_variables_and_types() -> None:
    section("1. Variables & Dynamic Typing")

    # Python infers types automatically
    user_name = "Alex"
    user_age = 28
    hourly_rate = 45.75
    is_active = True
    project_notes = None

    print(f"Name:        {user_name} (Type: {type(user_name).__name__})")
    print(f"Age:         {user_age} (Type: {type(user_age).__name__})")
    print(f"Hourly Rate: {hourly_rate} (Type: {type(hourly_rate).__name__})")
    print(f"Active:      {is_active} (Type: {type(is_active).__name__})")
    print(f"Notes:       {project_notes} (Type: {type(project_notes).__name__})")

    # Dynamic retyping demonstration
    flexible_var = 100
    print(f"\nflexible_var initial: {flexible_var} -> {type(flexible_var).__name__}")
    flexible_var = "Now I am a string!"
    print(f"flexible_var reassigned: {flexible_var} -> {type(flexible_var).__name__}")


def demo_type_casting() -> None:
    section("2. Type Checking & Casting")

    numeric_str = "125"
    converted_int = int(numeric_str)
    converted_float = float(numeric_str)

    print(f"Original String: '{numeric_str}'")
    print(f"Casted to int:    {converted_int} (isinstance int? {isinstance(converted_int, int)})")
    print(f"Casted to float:  {converted_float} (isinstance float? {isinstance(converted_float, float)})")

    # Truthy and Falsy conversions
    print("\nTruthy & Falsy Values in Python:")
    falsy_values = [0, 0.0, "", None, [], {}, set()]
    for val in falsy_values:
        print(f"  bool({repr(val):<10}) => {bool(val)}")

    truthy_sample = ["hello", 42, [1, 2]]
    for val in truthy_sample:
        print(f"  bool({repr(val):<10}) => {bool(val)}")


def demo_arithmetic_operators() -> None:
    section("3. Arithmetic Operators")

    a = 17
    b = 5

    print(f"Given a = {a}, b = {b}:")
    print(f"  Addition (a + b):         {a + b}")
    print(f"  Subtraction (a - b):      {a - b}")
    print(f"  Multiplication (a * b):   {a * b}")
    print(f"  True Division (a / b):    {a / b} (Always float)")
    print(f"  Floor Division (a // b):  {a // b} (Discards fractional part)")
    print(f"  Modulo (a % b):           {a % b} (Remainder)")
    print(f"  Exponentiation (a ** b):  {a ** b} (17 to the power of 5)")


def demo_strings_and_formatting() -> None:
    section("4. Strings & Advanced F-Strings")

    raw_text = "   python programming mastery   "
    print(f"Raw string:      '{raw_text}'")
    print(f"Cleaned (strip): '{raw_text.strip()}'")
    print(f"Uppercase:       '{raw_text.strip().upper()}'")
    print(f"Title Case:      '{raw_text.strip().title()}'")
    print(f"Replaced:        '{raw_text.strip().replace('python', 'advanced python')}'")

    # Splitting and Joining
    skills_list = ["Python", "FastAPI", "PostgreSQL", "Docker"]
    joined_skills = " -> ".join(skills_list)
    print(f"Joined Skills:   {joined_skills}")
    print(f"Split back:      {joined_skills.split(' -> ')}")

    # F-string formatting power
    revenue = 145920.789
    percentage = 0.8542
    print("\nFormatted F-strings:")
    print(f"  Currency:   ${revenue:,.2f}")
    print(f"  Percentage: {percentage:.1%}")
    print(f"  Padded Hex: 0x{255:04X}")
    print(f"  Inline math: 2 + 3 * 4 = {2 + 3 * 4}")


def demo_print_options() -> None:
    section("5. Print Formatting (sep & end)")

    print("Items separated by custom dashes:")
    print("Apple", "Banana", "Cherry", sep=" --- ")

    print("\nCustom line endings (simulating a progress bar):")
    for step in range(1, 6):
        print(f"[{step}/5]", end=" ... ")
    print("Done!")


def main() -> None:
    print("╔═══════════════════════════════════════════════╗")
    print("║      Part 01: Python Basics & Syntax          ║")
    print("╚═══════════════════════════════════════════════╝")

    demo_variables_and_types()
    demo_type_casting()
    demo_arithmetic_operators()
    demo_strings_and_formatting()
    demo_print_options()

    print("\n✅ Part 01 execution complete!")


if __name__ == "__main__":
    main()
