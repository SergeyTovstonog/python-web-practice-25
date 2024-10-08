from abc import ABC, abstractmethod
from math import pi


class Shape(ABC):

    @abstractmethod
    def area_of(self):
        pass


class Rect(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    # def area_of(self):
    #     return self.width * self.height


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area_of(self):
        return self.side ** 2


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area_of(self):
        return self.radius ** 2 * pi


class AreaCalculator:
    def __init__(self, shapes: list[Shape]):
        self.shapes = shapes

    def total_area(self) -> float:
        sum_ = 0
        for shape in self.shapes:
            sum_ += shape.area_of()
        return sum_


if __name__ == '__main__':
    ar_sh = AreaCalculator([Rect(10, 10), Rect(4, 5), Circle(20), Rect(3, 3), Square(10)])
    area = ar_sh.total_area()
    print(area)
