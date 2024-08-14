from abc import ABC, abstractmethod, ABCMeta


class Abs:

    def pay(self):
        raise NotImplementedError

class System(Abs):
    pass

class AbsAbstract(metaclass=ABCMeta):

    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def refund(self):
        pass



class

class SystemAbs(AbsAbstract):
    pass

if __name__ == '__main__':

    p = System()
    p1 = SystemAbs()