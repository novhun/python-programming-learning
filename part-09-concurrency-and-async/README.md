# Part 09: Concurrency, Multithreading & Asyncio

Modern applications often spend significant time waiting on external network services, disk I/O, or performing heavy computations. Python offers three primary paradigms for concurrent execution: **Multithreading**, **Multiprocessing**, and **Asyncio**. Understanding when and how to apply each is vital.

---

## 📖 Key Topics

### 1. The Global Interpreter Lock (GIL)
- In CPython, the GIL is a mutex preventing multiple native threads from executing Python bytecode simultaneously.
- **I/O-Bound Workloads**: Time is spent waiting for network or disk. Threads yield the GIL while waiting, making **Threading** or **Asyncio** ideal.
- **CPU-Bound Workloads**: Time is spent crunching numbers. Threads cannot utilize multiple CPU cores due to the GIL; use **Multiprocessing** instead.

### 2. Threading & Synchronization
- Provided by the `threading` module.
- Threads share the same memory space.
- **Race Conditions**: When two threads modify shared data simultaneously.
- **Locks (`threading.Lock`)**: Prevent race conditions via mutual exclusion:
  ```python
  import threading
  lock = threading.Lock()
  with lock:
      shared_balance += 10
  ```

### 3. ThreadPoolExecutor & ProcessPoolExecutor
- High-level abstractions in `concurrent.futures`:
  ```python
  from concurrent.futures import ThreadPoolExecutor

  with ThreadPoolExecutor(max_workers=5) as executor:
      results = list(executor.map(fetch_url, url_list))
  ```

### 4. Asynchronous Programming (`asyncio`)
- Single-threaded, cooperative multitasking driven by an **Event Loop**.
- Functions declared with `async def` are **coroutines**.
- The `await` keyword pauses execution of the current coroutine until the awaited task completes, yielding control back to the event loop to run other coroutines.
- Running concurrent coroutines:
  ```python
  results = await asyncio.gather(task_one(), task_two(), task_three())
  ```
- **Async Queue (`asyncio.Queue`)**: Enables elegant producer-consumer architectures.

---

## 🏃‍♂️ How to Run the Code

Run the accompanying script from your terminal:

```bash
python3 part-09-concurrency-and-async/main.py
```

---

## ✍️ Practice Exercises

1. **Async Web Scraping Simulator**: Simulate scraping 10 URLs asynchronously with random delays using `asyncio.sleep()`. Track start, end, and total elapsed time with `asyncio.gather()`.
2. **Producer-Consumer Pipeline**: Build an `asyncio.Queue` pipeline with 2 producer coroutines generating mock IoT sensor readings and 3 consumer coroutines processing and storing the readings.
3. **Thread-Safe Bank Account**: Create a shared bank account and 10 threads trying to deposit and withdraw money simultaneously. Verify that race conditions corrupt the balance without locks, and that `threading.Lock` preserves balance accuracy.
