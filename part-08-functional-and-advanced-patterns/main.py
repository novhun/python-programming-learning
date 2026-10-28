#!/usr/bin/env python3
"""
Part 08: Functional & Advanced Patterns
-----------------------------------------
This runnable script demonstrates:
1. Custom Iterators (__iter__ and __next__)
2. Generators and Generator Pipelines (yield)
3. Custom Decorators (with arguments and wraps)
4. Class-based Decorators
5. functools (lru_cache memoization, partial)
6. itertools (chain, islice, accumulate)
"""

from __future__ import annotations
import functools
import itertools
import time
from typing import Any, Callable


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


# --- 1. Custom Iterator ---
class NumberRangeIterator:
    """Demonstrates the Iterator Protocol."""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> NumberRangeIterator:
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        val = self.current
        self.current += self.step
        return val


def demo_iterators() -> None:
    section("1. Iterator Protocol (__iter__ & __next__)")

    custom_seq = NumberRangeIterator(10, 25, step=5)
    print("Iterating over custom NumberRangeIterator(10, 25, step=5):")
    for num in custom_seq:
        print(f"  Received: {num}")


# --- 2. Generators & Pipelines ---
def infinite_fibonacci():
    """Infinite Fibonacci generator yielding on demand."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def filter_even_stream(numbers):
    """Generator stage: filters even numbers."""
    for n in numbers:
        if n % 2 == 0:
            yield n


def square_stream(numbers):
    """Generator stage: squares incoming numbers."""
    for n in numbers:
        yield n * n


def demo_generators() -> None:
    section("2. Generators & Processing Pipelines")

    fib_gen = infinite_fibonacci()
    print("First 8 Fibonacci numbers via itertools.islice:")
    first_8 = list(itertools.islice(fib_gen, 8))
    print(f"  {first_8}")

    print("\nStreaming Generator Pipeline (Source -> Filter Even -> Square):")
    raw_source = range(1, 11)  # 1 to 10
    evens = filter_even_stream(raw_source)
    squared_evens = square_stream(evens)

    for item in squared_evens:
        print(f"  Processed through pipeline: {item}")


# --- 3. Decorators ---
def measure_time(func: Callable) -> Callable:
    """Decorator measuring execution time."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration_ms = (time.perf_counter() - start) * 1000
        print(f"  [@measure_time] {func.__name__} took {duration_ms:.3f} ms")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 0.05):
    """Decorator with arguments to retry transient failures."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    attempts += 1
                    print(f"  [@retry] Attempt {attempts}/{max_attempts} failed ({err}). Retrying in {delay}s...")
                    time.sleep(delay)
            raise RuntimeError(f"Function '{func.__name__}' failed after {max_attempts} attempts.")
        return wrapper
    return decorator


class CallCounter:
    """Class-based decorator tracking invocation count."""
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.count = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.count += 1
        print(f"  [CallCounter] {self.func.__name__} called {self.count} time(s).")
        return self.func(*args, **kwargs)


@measure_time
def compute_heavy_task() -> int:
    return sum(x * x for x in range(300_000))


_transient_failures = 2


@retry(max_attempts=4, delay=0.01)
def unreliable_network_call() -> str:
    global _transient_failures
    if _transient_failures > 0:
        _transient_failures -= 1
        raise ConnectionResetError("Connection dropped by remote host")
    return "Data payload received successfully!"


@CallCounter
def greet_user(name: str) -> str:
    return f"Hello, {name}!"


def demo_decorators() -> None:
    section("3. Decorators (Timing, Retries, and Class-based)")

    print("Executing timed function:")
    res = compute_heavy_task()
    print(f"  Result: {res}")

    print("\nExecuting retry function:")
    net_result = unreliable_network_call()
    print(f"  Outcome: {net_result}")

    print("\nExecuting class-based decorated function:")
    print(f"  {greet_user('Alice')}")
    print(f"  {greet_user('Bob')}")


# --- 4. functools & itertools ---
@functools.lru_cache(maxsize=128)
def cached_fibonacci(n: int) -> int:
    """Compute Fibonacci with dynamic programming memoization."""
    if n < 2:
        return n
    return cached_fibonacci(n - 1) + cached_fibonacci(n - 2)


def demo_functools_and_itertools() -> None:
    section("4. functools (lru_cache, partial) & itertools")

    # lru_cache benchmark
    start = time.perf_counter()
    fib_35 = cached_fibonacci(35)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"Fibonacci(35) computed via @lru_cache: {fib_35} in {elapsed:.3f} ms")
    print(f"Cache statistics: {cached_fibonacci.cache_info()}")

    # functools.partial
    def power(base: int, exponent: int) -> int:
        return base ** exponent

    square = functools.partial(power, exponent=2)
    cube = functools.partial(power, exponent=3)

    print(f"\nPartial application:")
    print(f"  square(5) = {square(5)}")
    print(f"  cube(3)   = {cube(3)}")

    # itertools demonstration
    print("\nItertools utilities:")
    chained = list(itertools.chain([1, 2, 3], ["a", "b", "c"]))
    print(f"  itertools.chain:     {chained}")

    running_sum = list(itertools.accumulate([1, 2, 3, 4, 5]))
    print(f"  itertools.accumulate: {running_sum}")


def main() -> None:
    print("╔═══════════════════════════════════════════════╗")
    print("║   Part 08: Functional & Advanced Patterns     ║")
    print("╚═══════════════════════════════════════════════╝")

    demo_iterators()
    demo_generators()
    demo_decorators()
    demo_functools_and_itertools()

    print("\n✅ Part 08 execution complete!")


if __name__ == "__main__":
    main()
