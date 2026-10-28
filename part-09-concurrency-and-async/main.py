#!/usr/bin/env python3
"""
Part 09: Concurrency, Multithreading & Asyncio
------------------------------------------------
This runnable script demonstrates:
1. Multithreading & Thread Synchronization with Locks
2. ThreadPoolExecutor for concurrent worker pools
3. Asynchronous programming with asyncio (coroutine execution, asyncio.gather)
4. Async Producer-Consumer queue pipeline
"""

from __future__ import annotations
import asyncio
from concurrent.futures import ThreadPoolExecutor
import random
import threading
import time


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


# --- 1. Multithreading & Thread Safety ---
class ThreadSafeCounter:
    def __init__(self) -> None:
        self.value = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:  # Mutual exclusion lock
            # Critical Section
            current = self.value
            time.sleep(0.0001)  # Simulate small context switch window
            self.value = current + 1


def demo_multithreading() -> None:
    section("1. Multithreading & Thread Synchronization (Lock)")

    counter = ThreadSafeCounter()
    threads: list[threading.Thread] = []
    worker_count = 10
    increments_per_thread = 50

    def worker() -> None:
        for _ in range(increments_per_thread):
            counter.increment()

    # Spawn 10 concurrent threads
    for _ in range(worker_count):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    expected = worker_count * increments_per_thread
    print(f"Total Threads: {worker_count}, Increments each: {increments_per_thread}")
    print(f"Final Counter Value: {counter.value} (Expected: {expected}) -> Thread-Safe!")


# --- 2. Concurrent Futures (ThreadPoolExecutor) ---
def simulated_download(task_id: int) -> str:
    delay = 0.05 + random.random() * 0.05
    time.sleep(delay)
    return f"Download #{task_id} completed in {delay * 1000:.1f}ms"


def demo_thread_pool() -> None:
    section("2. ThreadPoolExecutor (I/O Concurrency)")

    start = time.perf_counter()
    tasks = list(range(1, 6))

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(simulated_download, tasks))

    elapsed = (time.perf_counter() - start) * 1000
    print("Results from pool of 3 worker threads:")
    for res in results:
        print(f"  {res}")
    print(f"Total concurrent time: {elapsed:.1f}ms (vs ~{sum(50 for _ in tasks):.0f}ms sequential)")


# --- 3. Asynchronous Programming (asyncio) ---
async def fetch_service_data(service_name: str, delay: float) -> dict[str, str | float]:
    print(f"  [Async] Request sent to {service_name}...")
    await asyncio.sleep(delay)  # Yields control back to the event loop
    print(f"  [Async] Response received from {service_name}!")
    return {"service": service_name, "latency_ms": delay * 1000}


async def demo_asyncio_gather() -> None:
    section("3. Asyncio Coroutines & asyncio.gather")

    start = time.perf_counter()
    # Execute 3 network requests concurrently on a single thread
    results = await asyncio.gather(
        fetch_service_data("Auth-Service", 0.08),
        fetch_service_data("Payment-Service", 0.05),
        fetch_service_data("Inventory-Service", 0.10),
    )

    total_time = (time.perf_counter() - start) * 1000
    print(f"\nAll services responded in {total_time:.1f}ms:")
    for item in results:
        print(f"  Service: {item['service']:<18} | Latency: {item['latency_ms']:.1f}ms")


# --- 4. Async Producer-Consumer Pipeline ---
async def producer(queue: asyncio.Queue[str | None], producer_id: int, item_count: int) -> None:
    for i in range(1, item_count + 1):
        item = f"Job-{producer_id}.{i}"
        await asyncio.sleep(0.01)
        await queue.put(item)
        print(f"    [Producer {producer_id}] Produced {item}")


async def consumer(queue: asyncio.Queue[str | None], consumer_id: int) -> None:
    while True:
        item = await queue.get()
        if item is None:  # Sentinel value indicating completion
            queue.task_done()
            break
        print(f"      [Consumer {consumer_id}] Processing {item}...")
        await asyncio.sleep(0.02)
        queue.task_done()


async def demo_async_pipeline() -> None:
    section("4. Async Producer-Consumer Queue Pipeline")

    queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=10)

    # Launch 2 consumers
    consumer_tasks = [
        asyncio.create_task(consumer(queue, 1)),
        asyncio.create_task(consumer(queue, 2)),
    ]

    # Launch 2 producers and wait for them to finish
    await asyncio.gather(
        producer(queue, 1, 3),
        producer(queue, 2, 3),
    )

    # Wait until all items in the queue are processed
    await queue.join()

    # Send stop signals to consumers
    for _ in consumer_tasks:
        await queue.put(None)
    await asyncio.gather(*consumer_tasks)

    print("  Pipeline drained and shut down cleanly.")


async def async_main() -> None:
    await demo_asyncio_gather()
    await demo_async_pipeline()


def main() -> None:
    print("╔═══════════════════════════════════════════════╗")
    print("║     Part 09: Concurrency & Asyncio            ║")
    print("╚═══════════════════════════════════════════════╝")

    demo_multithreading()
    demo_thread_pool()
    asyncio.run(async_main())

    print("\n✅ Part 09 execution complete!")


if __name__ == "__main__":
    main()
