import random
from abc import abstractmethod, ABC
import numpy as np


class Color:
    def __init__(self, r, g, b, a):
        self.validate_color(r, "r")
        self.validate_color(g, "g")
        self.validate_color(b, "b")
        self.validate_color(a, "a")

        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def get_color_rgba(self):
        return self.r, self.g, self.b, self.a

    def get_color_rgb(self):
        return self.r, self.g, self.b

    def set_color(self, r, g, b, a):
        self.validate_color(r, "r")
        self.validate_color(g, "g")
        self.validate_color(b, "b")
        self.validate_color(a, "a")

        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def validate_color(self, value, component):
        if not isinstance(value, (int, float)) or value < 0 or value > 255:
            raise ValueError(f"Il canale {component} deve essere compreso tra 0 e 255, hai dato {value}")

    def randomize_by_range(self,
                           range_value):  # Fatto usando numpy perchè normalmente lagga troppo, python mi fa vomitare
        variations = np.random.uniform(-range_value, range_value, size=4)

        new_colors = np.array([self.r, self.g, self.b, self.a]) + variations

        new_colors = np.clip(new_colors, 0, 255)

        self.set_color(*new_colors)


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, x, y):
        self.x = x
        self.y = y


class ParticleI(ABC):  # Pro tip, mai cercare di fare le classi astratte in python, fanno pena
    @property
    @abstractmethod
    def color(self) -> Color:
        pass

    @property
    @abstractmethod
    def pos(self) -> Vector2:
        pass

    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @property
    @abstractmethod
    def density(self) -> float:
        pass

    @abstractmethod
    def apply_rules(self, grid):
        pass

    @abstractmethod
    def set_pos(self, new_pos: Vector2):
        pass

    @abstractmethod
    def set_color(self, color: Color):
        pass
