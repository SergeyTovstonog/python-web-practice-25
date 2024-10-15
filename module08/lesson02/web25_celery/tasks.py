# tasks.py
from celery_app import app
import time

@app.task
def add(x, y):
    result = x + y
    print(f"Adding {x} + {y} = {result}")
    return result

@app.task
def multiply(x, y):
    result = x * y
    print(f"Multiplying {x} * {y} = {result}")
    return result

@app.task
def long_task():
    print("Starting a long task...")
    time.sleep(10)
    print("Long task completed.")
    return "Done"
