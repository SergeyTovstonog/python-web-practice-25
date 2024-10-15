import time
import redis
from redis_lru import RedisLRU
from functools import lru_cache



# ============================
# Configuration and Setup
# ============================

# Redis server configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
CACHE_MAXSIZE = 100  # Maximum number of items to store in the cache

# Create a Redis client
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    # Test the connection
    redis_client.ping()
    print("Connected to Redis successfully.")
except redis.exceptions.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")
    exit(1)

# Initialize RedisLRU with the Redis client and maximum cache size
cache = RedisLRU(redis_client)


# ============================
# Cached Function Definition
# ============================


def get_data_cached(key):
    return get_data(key)


# ============================
@cache()
def get_data(key):
    """
    Simulates a time-consuming data retrieval operation.

    Args:
        key (str): The key for which to retrieve data.

    Returns:
        str: Simulated data corresponding to the key.
    """
    print(f"Fetching data for '{key}' from the source...")
    time.sleep(2)  # Simulate delay (e.g., fetching from an external API)
    return f"Data for '{key}'"


# ============================
# Main Execution
# ============================

def main():
    test_keys = ["apple", "banana", "apple", "banana", "cherry", "apple"]

    for i, key in enumerate(test_keys, start=1):
        print(f"\nCall {i}: Retrieving data for '{key}'")
        start_time = time.time()
        result = get_data(key)
        elapsed_time = time.time() - start_time
        print(f"Result: {result}")
        print(f"Time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
