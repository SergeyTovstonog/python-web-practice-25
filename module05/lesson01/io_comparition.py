import concurrent.futures
import time
import asyncio

# Simulated task (synchronous)
def task(n):
    print(f"Task {n} started (sync)")
    time.sleep(2)  # Simulate a delay
    print(f"Task {n} completed (sync)")
    return n * 2

# Simulated task (asynchronous)
async def async_task(n):
    print(f"Task {n} started (async)")
    await asyncio.sleep(2)  # Simulate a delay asynchronously
    print(f"Task {n} completed (async)")
    return n * 2

# Sequential execution
def sequential_execution(tasks):
    print("\nSequential execution:")
    results = []
    for n in tasks:
        result = task(n)
        results.append(result)
    return results

# ThreadPoolExecutor execution
def thread_pool_execution(tasks):
    print("\nThread pool execution:")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = [executor.submit(task, n) for n in tasks]
        return [future.result() for future in concurrent.futures.as_completed(results)]

# Asyncio execution
async def asyncio_execution(tasks):
    print("\nAsyncio execution:")
    coroutines = [async_task(n) for n in tasks]
    return await asyncio.gather(*coroutines)

# Main function to compare the methods
def main():
    tasks = [n for n in range(10)]

    # Sequential execution
    start_time = time.time()
    sequential_results = sequential_execution(tasks)
    print(f"Results (sequential): {sequential_results}")
    print(f"Sequential execution time: {time.time() - start_time:.2f} seconds")

    # ThreadPoolExecutor execution
    start_time = time.time()
    thread_pool_results = thread_pool_execution(tasks)
    print(f"Results (thread pool): {thread_pool_results}")
    print(f"Thread pool execution time: {time.time() - start_time:.2f} seconds")

    # Asyncio execution
    start_time = time.time()
    asyncio_results = asyncio.run(asyncio_execution(tasks))
    print(f"Results (asyncio): {asyncio_results}")
    print(f"Asyncio execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
