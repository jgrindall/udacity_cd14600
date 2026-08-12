class AShape:
    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError("Subclasses must implement this method")

    def perimeter(self):
        raise NotImplementedError("Subclasses must implement this method")



class RectShape(AShape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class CircleShape(AShape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type, *args):
        if shape_type == "rectangle":
            return RectShape(*args)
        elif shape_type == "circle":
            return CircleShape(*args)
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")



