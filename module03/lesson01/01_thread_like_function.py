
from random import randrange
from threading import Thread
from time import sleep


def worker(param):
    sleep(randrange(5))
    print(param)


if __name__ == '__main__':
    threads = []
    for i in range(5):
        th = Thread(target=worker, args=(f"Count thread - {i}", ))
        threads.append(th)
        th.start()

    for th in threads:
        th.join()
    sleep(2)
    print("MainThread finished")
