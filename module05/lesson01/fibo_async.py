import time
import threading
import multiprocessing
import asyncio

# Function to calculate Fibonacci sequence (recursive, CPU-bound)
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Sequential approach
def sequential_fibonacci(numbers):
    fib_results = []
    start_time = time.time()
    for number in numbers:
        fib_results.append(fibonacci(number))
    end_time = time.time()
    print("Sequential execution time:", end_time - start_time)

# Multithreading approach
def multithreading_fibonacci(numbers):
    start_time = time.time()
    threads = []
    fib_results = []

    # Define a function to be executed by each thread
    def worker(number):
        fib_results.append(fibonacci(number))

    # Create and start a thread for each number
    for number in numbers:
        thread = threading.Thread(target=worker, args=(number,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    end_time = time.time()
    print("Multithreading execution time:", end_time - start_time)

# Multiprocessing approach
def multiprocessing_fibonacci(numbers):
    start_time = time.time()
    with multiprocessing.Pool() as pool:
        fib_results = pool.map(fibonacci, numbers)
    end_time = time.time()
    print("Multiprocessing execution time:", end_time - start_time)

# Asynchronous Fibonacci function
async def async_fibonacci(n):
    if n <= 1:
        return n
    else:
        # Awaiting the result of recursive calls (simulating async)
        return await async_fibonacci(n-1) + await async_fibonacci(n-2)

# Asynchronous approach
async def async_fibonacci_runner(numbers):
    start_time = time.time()
    tasks = [async_fibonacci(number) for number in numbers]
    fib_results = await asyncio.gather(*tasks)
    end_time = time.time()
    print("Asynchronous execution time:", end_time - start_time)
    return fib_results

if __name__ == "__main__":
    numbers = [35] * 10  # Calculate Fibonacci(35) for 10 times

    # Sequential execution
    sequential_fibonacci(numbers)

    # Multithreading execution
    multithreading_fibonacci(numbers)

    # Multiprocessing execution
    multiprocessing_fibonacci(numbers)

    # Asynchronous execution
    asyncio.run(async_fibonacci_runner(numbers))
