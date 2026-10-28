#!/usr/bin/env python3
"""
Part 04: Functions, Scopes & Modules
------------------------------------
This runnable script demonstrates:
1. Advanced function signatures (positional-only, keyword-only, *args, **kwargs)
2. The mutable default argument trap & the idiomatic fix
3. Variable scope and LEGB resolution (global and nonlocal keywords)
4. Closures and factory functions
5. Functional programming (map, filter, reduce, lambdas)
6. Module importing and interaction with math_operations.py
"""

from __future__ import annotations
from functools import reduce
from typing import Callable, Optional

# Import functions from our custom module
from math_operations import calculate_mean, calculate_median, factorial


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def demo_function_signatures() -> None:
    section("1. Advanced Function Signatures")

    # / specifies positional-only arguments; * specifies keyword-only arguments
    def build_url(protocol: str, domain: str, /, path: str = "", *, port: int = 80, secure: bool = False) -> str:
        scheme = "https" if secure else protocol
        port_str = f":{port}" if port not in (80, 443) else ""
        return f"{scheme}://{domain}{port_str}/{path.lstrip('/')}"

    # protocol and domain MUST be positional
    # port and secure MUST be keyword arguments
    url1 = build_url("http", "api.example.com", "v1/users", secure=True)
    url2 = build_url("http", "localhost", "metrics", port=9090, secure=False)

    print(f"URL 1: {url1}")
    print(f"URL 2: {url2}")

    # *args and **kwargs in action
    def flexible_logger(prefix: str, *messages: str, **metadata: object) -> None:
        combined_msg = " ".join(messages)
        meta_str = " | ".join(f"{k}={v}" for k, v in metadata.items())
        print(f"[{prefix.upper()}] {combined_msg} (Context: {meta_str})")

    flexible_logger("info", "Database", "connection", "established", host="db-prod-1", retries=3)


def demo_mutable_default_pitfall() -> None:
    section("2. The Mutable Default Argument Trap")

    # BUGGY pattern: list default created once at def time
    def buggy_append(item: str, target_list: list[str] = []) -> list[str]:  # noqa: B006
        target_list.append(item)
        return target_list

    # IDIOMATIC pattern: use None sentinel
    def safe_append(item: str, target_list: list[str] | None = None) -> list[str]:
        if target_list is None:
            target_list = []
        target_list.append(item)
        return target_list

    print("Buggy function calls:")
    print("  Call 1:", buggy_append("item 1"))
    print("  Call 2:", buggy_append("item 2"), " <-- Notice state persisted from Call 1!")

    print("\nSafe function calls with None default:")
    print("  Call 1:", safe_append("item 1"))
    print("  Call 2:", safe_append("item 2"), " <-- Fresh isolated list each time!")


# Module-level global variable for scope demo
app_environment = "production"


def demo_scope_and_closures() -> None:
    section("3. Scope (LEGB) & Closures (nonlocal)")

    print(f"Initial global app_environment: {app_environment}")

    def modify_global_demo() -> None:
        global app_environment
        app_environment = "staging"

    modify_global_demo()
    print(f"Updated global app_environment: {app_environment}")

    # Closures & nonlocal demonstration
    def make_counter(start: int = 0) -> Callable[[], int]:
        count = start

        def increment() -> int:
            nonlocal count  # References the enclosing scope
            count += 1
            return count

        return increment

    counter_a = make_counter(10)
    counter_b = make_counter(100)

    print("\nClosure Counters:")
    print(f"  Counter A (starts at 10): {counter_a()}, {counter_a()}, {counter_a()}")
    print(f"  Counter B (starts at 100): {counter_b()}, {counter_b()}")


def demo_functional_programming() -> None:
    section("4. Functional Tools: map, filter, reduce & lambdas")

    scores = [45, 88, 72, 91, 58, 64, 99, 82]
    print(f"Original Scores: {scores}")

    # filter: passing scores (>= 70)
    passing_scores = list(filter(lambda s: s >= 70, scores))
    print(f"Passing Scores (>=70): {passing_scores}")

    # map: curve scores by +5 points (capped at 100)
    curved_scores = list(map(lambda s: min(100, s + 5), passing_scores))
    print(f"Curved Scores (+5):   {curved_scores}")

    # reduce: sum all curved scores
    total = reduce(lambda acc, val: acc + val, curved_scores, 0)
    print(f"Sum of Curved Scores: {total}")


def demo_custom_module_import() -> None:
    section("5. Using the Custom Module (math_operations.py)")

    dataset = [14.5, 22.0, 18.2, 35.7, 40.1, 19.8]
    print(f"Dataset: {dataset}")
    print(f"Mean:     {calculate_mean(dataset):.2f}")
    print(f"Median:   {calculate_median(dataset):.2f}")
    print(f"6! (Factorial): {factorial(6)}")


def main() -> None:
    print("╔═══════════════════════════════════════════════╗")
    print("║     Part 04: Functions, Scopes & Modules      ║")
    print("╚═══════════════════════════════════════════════╝")

    demo_function_signatures()
    demo_mutable_default_pitfall()
    demo_scope_and_closures()
    demo_functional_programming()
    demo_custom_module_import()

    print("\n✅ Part 04 execution complete!")


if __name__ == "__main__":
    main()
