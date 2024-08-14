import threading
import time
from datetime import datetime

import requests


# Function to fetch data from API
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Function to collect data using multithreading
def collect_data_with_threads(urls):
    threads = []
    results = []

    # Define a function to be executed by each thread
    def worker(url):
        data = fetch_data(url)
        # print(url)
        results.append(data)

    # Create and start a thread for each URL
    for url in urls:
        thread = threading.Thread(target=worker, args=(url,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return results


# Example usage
if __name__ == "__main__":
    # Example APIs

    apis = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(50)]

    print(f"Getting data for {len(apis)} URLs")

    # Collect data without threads

    # start_time = datetime.now()
    # data_without_threads = [fetch_data(api) for api in apis]
    # print("Data without threads:", data_without_threads)
    # end_time = datetime.now()
    # print(f"one by one - {end_time - start_time}")

    # Collect data with threads
    start_time = datetime.now()
    data_with_threads = collect_data_with_threads(apis)
    print("Data with threads:", data_with_threads)
    end_time = datetime.now()
    print(f"in threads - {end_time - start_time}")
