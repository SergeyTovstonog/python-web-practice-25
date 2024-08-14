from dataclasses import dataclass

# Пример применения синглтона -> подключение к БД из любого места программы


class MetaSingleton(type):
    __instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instance:
            cls.__instance[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls.__instance[cls]


# Показать dataclass
@dataclass
class Settings(metaclass=MetaSingleton):
    db: str = "MySQL"
    port: int = 3306


if __name__ == '__main__':

    connect = Settings()

    connect_other = Settings()

    print(connect_other.port)
    connect.port = 5634
    print(connect_other.port)



class Single:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

class InheritSingle(Single):
    pass


if __name__ == '__main__':
    s1 = Single()
    s2 = Single()
    print(s1 == s2)

    s3 = InheritSingle()
    s4 = InheritSingle()
    print(s3 == s4)