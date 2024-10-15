# run_tasks.py
from tasks import add, multiply, long_task


if __name__ == '__main__':
    result = add.delay(10, 20)
    sum_result = result.get(timeout=10)
    print(sum_result)
    multiply.delay(5, 7)
    long_task.delay()
