from functools import wraps
from collections
from itertools


def greeting(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("hello")
        result = func(*args, **kwargs)
        return result
    return wrapper

@greeting("Hi")
def person(name: str):
    """
    Print person's name
    """
    print(name)

def send_to_crm():
    ...

@send_to_crm("payment")
def payment():
    ...



if __name__ == '__main__':
    person("John")
    print(person.__name__)
    print(person.__doc__)
    print(person.__annotations__)

    person()

