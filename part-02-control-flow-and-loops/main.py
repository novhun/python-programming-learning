#!/usr/bin/env python3
"""
Part 02: Control Flow & Loops
------------------------------
This runnable script demonstrates:
1. Conditionals, ternary expressions, and short-circuit evaluation
2. Value equality (==) vs Object identity (is)
3. Structural Pattern Matching (match-case) with guards
4. For and While loops with break, continue, and the loop 'else' clause
5. Built-in iteration helpers: range, enumerate, zip, reversed
"""


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def demo_conditionals_and_ternary() -> None:
    section("1. Conditionals & Ternary Operator")

    score = 85

    # Multi-branch conditional
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "F"

    # Ternary expression (inline conditional)
    standing = "Honor Roll" if score >= 80 else "Standard"

    print(f"Score: {score} -> Grade: {grade}, Academic Standing: {standing}")

    # Short-circuit evaluation demonstration
    print("\nShort-circuit Evaluation:")
    # The right-hand side won't be evaluated if left side satisfies condition
    def expensive_check() -> bool:
        print("  [Warning] expensive_check was called!")
        return True

    print("Evaluating: False and expensive_check()")
    result1 = False and expensive_check()
    print(f"Result: {result1} (Notice: function was NEVER called)")

    print("Evaluating: True or expensive_check()")
    result2 = True or expensive_check()
    print(f"Result: {result2} (Notice: function was NEVER called)")


def demo_identity_vs_equality() -> None:
    section("2. Object Identity (is) vs Value Equality (==)")

    list_a = [1, 2, 3]
    list_b = [1, 2, 3]
    list_c = list_a

    print(f"list_a: {list_a} (id: {id(list_a)})")
    print(f"list_b: {list_b} (id: {id(list_b)})")
    print(f"list_c: {list_c} (id: {id(list_c)})")

    print(f"\nlist_a == list_b? {list_a == list_b}  (Values are equal)")
    print(f"list_a is list_b? {list_a is list_b}  (Different objects in memory)")
    print(f"list_a is list_c? {list_a is list_c}  (Exact same memory reference)")

    # Idiomatic check for None
    val = None
    print(f"\nChecking None idiomatically: 'val is None' -> {val is None}")


def demo_pattern_matching() -> None:
    section("3. Structural Pattern Matching (match-case)")

    commands = [
        "help",
        "go north",
        "teleport 150 300",
        "attack boss with excalibur",
        "unknown_action",
    ]

    for raw_cmd in commands:
        parts = raw_cmd.split()
        match parts:
            case ["help"]:
                print(f"Command '{raw_cmd}' -> Displaying help manual.")
            case ["go", direction]:
                print(f"Command '{raw_cmd}' -> Moving player to {direction.upper()}.")
            case ["teleport", x, y]:
                print(f"Command '{raw_cmd}' -> Teleporting coordinates to X={x}, Y={y}.")
            case ["attack", target, "with", weapon] if weapon == "excalibur":
                print(f"Command '{raw_cmd}' -> CRITICAL HIT! Attacking {target} with legendary {weapon}!")
            case ["attack", target, "with", weapon]:
                print(f"Command '{raw_cmd}' -> Regular attack on {target} using {weapon}.")
            case _:
                print(f"Command '{raw_cmd}' -> Unrecognized action.")


def demo_loops_and_controls() -> None:
    section("4. While & For Loops with break, continue, and else")

    # While loop countdown
    print("While Loop Countdown:")
    counter = 3
    while counter > 0:
        print(f"  T-minus {counter}...")
        counter -= 1
    print("  Liftoff!")

    # For-else pattern: prime check / search
    print("\nFor-Else Search Pattern:")
    target_value = 7
    numbers = [2, 4, 6, 8, 10]

    for num in numbers:
        if num == target_value:
            print(f"  Found {target_value}!")
            break
    else:
        # Executes ONLY when no 'break' occurred
        print(f"  Loop finished completely: {target_value} was NOT found in the list.")


def demo_iteration_helpers() -> None:
    section("5. Iteration Helpers (enumerate, zip, reversed, range)")

    languages = ["Python", "Go", "Rust", "TypeScript"]
    creators = ["Guido van Rossum", "Robert Griesemer", "Graydon Hoare", "Anders Hejlsberg"]

    print("Enumerate (Index + Element):")
    for idx, lang in enumerate(languages, start=1):
        print(f"  Rank #{idx}: {lang}")

    print("\nZip (Pairing Sequences):")
    for lang, author in zip(languages, creators):
        print(f"  {lang:<12} created by {author}")

    print("\nReversed Sequence:")
    for lang in reversed(languages):
        print(f"  <- {lang}", end=" ")
    print()

    print("\nCustom Range Step (Even numbers 10 down to 0):")
    for n in range(10, -1, -2):
        print(f"  {n}", end=" ")
    print()


def main() -> None:
    print("╔═══════════════════════════════════════════════╗")
    print("║     Part 02: Control Flow & Loops             ║")
    print("╚═══════════════════════════════════════════════╝")

    demo_conditionals_and_ternary()
    demo_identity_vs_equality()
    demo_pattern_matching()
    demo_loops_and_controls()
    demo_iteration_helpers()

    print("\n✅ Part 02 execution complete!")


if __name__ == "__main__":
    main()
