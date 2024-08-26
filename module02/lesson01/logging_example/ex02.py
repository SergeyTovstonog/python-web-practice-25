from logger import get_logger

logger = get_logger(__name__)


def baz(b):
    sum = 0
    for i in range(10):
        sum += b * i
    logger.info("Start baz")
    logger.debug(f"b={b}")


def foo():
    logger.error("Ups i did it again")


if __name__ == "__main__":
    # logger.log(logging.DEBUG, "Start")
    baz(10)
    baz(100)
    baz(1000)
    foo()
