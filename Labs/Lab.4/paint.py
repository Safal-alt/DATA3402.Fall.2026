import math


# Canvas class from Lecture 9
class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]

    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]

    def v_line(self, x, y, h, **kargs):
        for i in range(x, x+h):
            self.set_pixel(i, y, **kargs)

    def h_line(self, x, y, w, **kargs):
        for i in range(y, y+w):
            self.set_pixel(x, i, **kargs)

    def line(self, x1, y1, x2, y2, **kargs):
        slope = (x2-x1) / (y2-y1)
        for y in range(y1, y2):
            x = x1 + int(slope * (y-y1))
            self.set_pixel(x, y, **kargs)

    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


class Shape:
    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def perimeter_points(self):
        raise NotImplementedError

    def contains(self, x, y):
        raise NotImplementedError

    def overlaps(self, other):
        for x, y in self.perimeter_points():
            if other.contains(x, y):
                return True

        for x, y in other.perimeter_points():
            if self.contains(x, y):
                return True

        return False

    def paint(self, canvas):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        self.__length = length
        self.__width = width
        self.__x = x
        self.__y = y

    def area(self):
        return self.__length * self.__width

    def perimeter(self):
        return 2 * (self.__length + self.__width)

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def perimeter_points(self):
        x = self.__x
        y = self.__y
        l = self.__length
        w = self.__width

        return [
            (x, y),
            (x + l, y),
            (x + l, y + w),
            (x, y + w)
        ]

    def contains(self, x, y):
        return (
            self.__x <= x <= self.__x + self.__length
            and self.__y <= y <= self.__y + self.__width
        )

    def paint(self, canvas):
        x = int(self.__x)
        y = int(self.__y)
        length = int(self.__length)
        width = int(self.__width)

        canvas.h_line(x, y, width, char='*')
        canvas.h_line(x + length, y, width, char='*')
        canvas.v_line(x, y, length, char='*')
        canvas.v_line(x, y + width - 1, length, char='*')

    # Added for Question 12
    def __repr__(self):
        return (
            f"Rectangle({repr(self.__length)}, "
            f"{repr(self.__width)}, "
            f"{repr(self.__x)}, "
            f"{repr(self.__y)})"
        )


class Circle(Shape):
    def __init__(self, radius, x, y):
        self.__radius = radius
        self.__x = x
        self.__y = y

    def area(self):
        return math.pi * self.__radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.__radius

    def get_radius(self):
        return self.__radius

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def perimeter_points(self):
        points = []

        for i in range(16):
            angle = 2 * math.pi * i / 16
            x = self.__x + self.__radius * math.cos(angle)
            y = self.__y + self.__radius * math.sin(angle)
            points.append((x, y))

        return points

    def contains(self, x, y):
        return (
            (x - self.__x)**2 +
            (y - self.__y)**2
            <= self.__radius**2
        )

    def paint(self, canvas):
        for x, y in self.perimeter_points():
            row = int(round(x))
            col = int(round(y))

            if 0 <= row < canvas.height and 0 <= col < canvas.width:
                canvas.set_pixel(row, col, char='o')

    # Added for Question 12
    def __repr__(self):
        return (
            f"Circle({repr(self.__radius)}, "
            f"{repr(self.__x)}, "
            f"{repr(self.__y)})"
        )


class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__x3 = x3
        self.__y3 = y3

    def area(self):
        return abs(
            self.__x1 * (self.__y2 - self.__y3)
            + self.__x2 * (self.__y3 - self.__y1)
            + self.__x3 * (self.__y1 - self.__y2)
        ) / 2

    def perimeter(self):
        side1 = math.sqrt(
            (self.__x2-self.__x1)**2 +
            (self.__y2-self.__y1)**2
        )

        side2 = math.sqrt(
            (self.__x3-self.__x2)**2 +
            (self.__y3-self.__y2)**2
        )

        side3 = math.sqrt(
            (self.__x1-self.__x3)**2 +
            (self.__y1-self.__y3)**2
        )

        return side1 + side2 + side3

    def get_x1(self):
        return self.__x1

    def get_y1(self):
        return self.__y1

    def get_x2(self):
        return self.__x2

    def get_y2(self):
        return self.__y2

    def get_x3(self):
        return self.__x3

    def get_y3(self):
        return self.__y3

    def perimeter_points(self):
        points = []

        vertices = [
            (self.__x1, self.__y1),
            (self.__x2, self.__y2),
            (self.__x3, self.__y3)
        ]

        for i in range(3):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % 3]

            for j in range(5):
                t = j / 5
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                points.append((x, y))

        return points

    def contains(self, x, y):
        def sign(px, py, ax, ay, bx, by):
            return (px-bx)*(ay-by) - (ax-bx)*(py-by)

        d1 = sign(
            x, y,
            self.__x1, self.__y1,
            self.__x2, self.__y2
        )

        d2 = sign(
            x, y,
            self.__x2, self.__y2,
            self.__x3, self.__y3
        )

        d3 = sign(
            x, y,
            self.__x3, self.__y3,
            self.__x1, self.__y1
        )

        has_negative = d1 < 0 or d2 < 0 or d3 < 0
        has_positive = d1 > 0 or d2 > 0 or d3 > 0

        return not (has_negative and has_positive)

    def paint(self, canvas):
        points = self.perimeter_points()

        for x, y in points:
            row = int(round(x))
            col = int(round(y))

            if 0 <= row < canvas.height and 0 <= col < canvas.width:
                canvas.set_pixel(row, col, char='+')

    # Added for Question 12
    def __repr__(self):
        return (
            f"Triangle({repr(self.__x1)}, {repr(self.__y1)}, "
            f"{repr(self.__x2)}, {repr(self.__y2)}, "
            f"{repr(self.__x3)}, {repr(self.__y3)})"
        )


class CompoundShape(Shape):
    def __init__(self):
        self.__shapes = []

    def add_shape(self, shape):
        self.__shapes.append(shape)

    def paint(self, canvas):
        for shape in self.__shapes:
            shape.paint(canvas)

    def get_shapes(self):
        return self.__shapes


class RasterDrawing:
    def __init__(self, shapes=None):
        if shapes is None:
            self.__shapes = []
        else:
            self.__shapes = shapes

    def add_shape(self, shape):
        self.__shapes.append(shape)

    def remove_shape(self, shape):
        self.__shapes.remove(shape)

    def paint(self, canvas):
        canvas.clear_canvas()

        for shape in self.__shapes:
            shape.paint(canvas)

    def get_shapes(self):
        return self.__shapes

    # Added for Question 12
    def __repr__(self):
        return f"RasterDrawing({repr(self.__shapes)})"

    # Added for Question 12
    def save(self, filename):
        f = open(filename, "w")
        f.write(self.__repr__())
        f.close()


# Added for Question 12
def load_raster_drawing(filename):
    f = open(filename, "r")
    drawing = eval(f.read())
    f.close()

    return drawing