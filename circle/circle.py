import math
class Circle:

    def __init__(self, radius=1):
        self.radius = radius

    def __repr__(self):
        return(f"Circle({self.__radius})")

    @property
    def radius(self):
        return self.__radius

    @property
    def diameter(self):
        return self.__radius * 2


    @property
    def area(self):
        return math.pi * (self.__radius ** 2)

    @radius.setter
    def radius(self, r):
        if r < 0:
            raise ValueError('Radius cannot be negative')
        else:
            self.__radius = r

    @diameter.setter
    def diameter(self, d):
        self.__radius = (d/2)