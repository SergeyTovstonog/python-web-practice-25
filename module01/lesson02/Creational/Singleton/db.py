from dataclasses import dataclass


class Connection:

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance


@dataclass
class MySQL(Connection):
    db: str = "MySQL"
    port: int = 3306

@dataclass
class MSSQL(Connection):
    db: str = "MSSQL"
    port: int = 1251

if __name__ == '__main__':

    db1 = MySQL()
    db2 = MSSQL()

    print(db2 is db1)