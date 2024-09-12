import asyncio
import time

async def brew_coffee():
    print("Brewing coffee...")
    await asyncio.sleep(3)  # Simulate time taken to brew coffee
    print("Coffee is ready!")

async def bake_toast():
    print("Baking toast...")
    await asyncio.sleep(2)  # Simulate time taken to bake toast
    print("Toast is ready!")

async def fry_eggs():
    print("Frying eggs...")
    await asyncio.sleep(4)  # Simulate time taken to fry eggs
    print("Eggs are ready!")

async def prepare_breakfast():
    # Prepare coffee, toast, and eggs concurrently
    await asyncio.gather(
        brew_coffee(),
        bake_toast(),
        fry_eggs()
    )
    print("Breakfast is ready!")

if __name__ == "__main__":
    start_time = time.time()  # Record the start time
    asyncio.run(prepare_breakfast())
    end_time = time.time()  # Record the end time
    total_time = end_time - start_time
    print(f"Total time taken: {total_time:.2f} seconds")
