from ParticleInterface import *
import random


class Sand(ParticleI):
    def __init__(self, x: float = 0, y: float = 0, id: int = 1):
        self._color = Color(194, 178, 128, 255)
        self.color.randomize_by_range(10)
        self._pos = Vector2(x, y)
        self._id = id
        self._density = 1.5

    @property
    def color(self) -> Color:
        return self._color

    @property
    def pos(self) -> Vector2:
        return self._pos

    @property
    def id(self) -> int:
        return self._id

    @property
    def density(self) -> float:
        return self._density

    def set_pos(self, new_pos: Vector2):
        self._pos = new_pos

    def set_color(self, color: Color):
        self._color = color

    def apply_rules(self, grid):
        x, y = self.pos.get_pos()
        grid_height, grid_width = grid.shape

        def is_valid(x: int, y: int) -> bool:
            return 0 <= x < grid_width and 0 <= y < grid_height

        def is_valid_and_empty(x: int, y: int) -> bool:
            return is_valid(x, y) and (grid[y, x] is None or grid[y, x].id == 0)

        # Gravità
        if is_valid_and_empty(x, y + 1):
            self.set_pos(Vector2(x, y + 1))
            return

        # Densità
        if is_valid(x, y + 1) and grid[y + 1, x] is not None and grid[y + 1, x].id != 0:
            other_particle = grid[y + 1, x]
            if self.density > other_particle.density:
                self.set_pos(Vector2(x, y + 1))
                other_particle.set_pos(Vector2(x, y))
                return

        # Gravità diagonale
        directions = [(x - 1, y + 1), (x + 1, y + 1)]
        random.shuffle(directions)
        for new_x, new_y in directions:
            if is_valid_and_empty(new_x, new_y):
                self.set_pos(Vector2(new_x, new_y))
                return
            # Diagonale densità
            if is_valid(new_x, new_y) and grid[new_y, new_x] is not None and grid[new_y, new_x].id != 0:
                other_particle = grid[new_y, new_x]
                if self.density > other_particle.density:
                    self.set_pos(Vector2(new_x, new_y))
                    other_particle.set_pos(Vector2(x, y))
                    return


class Water(ParticleI):
    def __init__(self, x: float = 0, y: float = 0, id: int = 2):
        self._color = Color(0, 105, 148, 255)
        self.color.randomize_by_range(10)
        self._pos = Vector2(x, y)
        self._id = id
        self._density = 1.0

    @property
    def color(self) -> Color:
        return self._color

    @property
    def pos(self) -> Vector2:
        return self._pos

    @property
    def id(self) -> int:
        return self._id

    @property
    def density(self) -> float:
        return self._density

    def set_pos(self, new_pos: Vector2):
        self._pos = new_pos

    def set_color(self, color: Color):
        self._color = color

    def apply_rules(self, grid):
        x, y = self.pos.get_pos()
        grid_height, grid_width = grid.shape

        def is_valid(x: int, y: int) -> bool:
            return 0 <= x < grid_width and 0 <= y < grid_height

        def is_valid_and_empty(x: int, y: int) -> bool:
            return is_valid(x, y) and (grid[y, x] is None or grid[y, x].id == 0)

        # Gravità
        if is_valid_and_empty(x, y + 1):
            self.set_pos(Vector2(x, y + 1))
            return

        # Densità verticale
        if is_valid(x, y + 1) and grid[y + 1, x] is not None and grid[y + 1, x].id != 0:
            other_particle = grid[y + 1, x]
            if self.density > other_particle.density:
                self.set_pos(Vector2(x, y + 1))
                other_particle.set_pos(Vector2(x, y))
                return

        # Orizzontale
        directions = [(x - 1, y), (x + 1, y)]
        random.shuffle(directions)
        for new_x, new_y in directions:
            if is_valid_and_empty(new_x, new_y):
                self.set_pos(Vector2(new_x, new_y))
                return
            # Densità orizzontale
            if is_valid(new_x, new_y) and grid[new_y, new_x] is not None and grid[new_y, new_x].id != 0:
                other_particle = grid[new_y, new_x]
                if self.density > other_particle.density:
                    self.set_pos(Vector2(new_x, new_y))
                    other_particle.set_pos(Vector2(x, y))
                    return


class Steam(ParticleI):
    def __init__(self, x: float = 0, y: float = 0, id: int = 3):
        self._color = Color(200, 200, 200, 128)
        self.color.randomize_by_range(10)
        self._pos = Vector2(x, y)
        self._id = id
        self._density = 0.3

    @property
    def color(self) -> Color:
        return self._color

    @property
    def pos(self) -> Vector2:
        return self._pos

    @property
    def id(self) -> int:
        return self._id

    @property
    def density(self) -> float:
        return self._density

    def set_pos(self, new_pos: Vector2):
        self._pos = new_pos

    def set_color(self, color: Color):
        self._color = color

    def apply_rules(self, grid):
        x, y = self.pos.get_pos()
        grid_height, grid_width = grid.shape

        def is_valid(x: int, y: int) -> bool:
            return 0 <= x < grid_width and 0 <= y < grid_height

        def is_valid_and_empty(x: int, y: int) -> bool:
            return is_valid(x, y) and (grid[y, x] is None or grid[y, x].id == 0)

        # Gravità (invertità perchè è gas)
        if y > 0 and is_valid_and_empty(x, y - 1):
            self.set_pos(Vector2(x, y - 1))
            return

        # Controllo orizzontale
        directions = [(x - 1, y), (x + 1, y)]
        random.shuffle(directions)
        for new_x, new_y in directions:
            if is_valid_and_empty(new_x, new_y):
                self.set_pos(Vector2(new_x, new_y))
                return


class Stone(ParticleI):
    def __init__(self, x: float = 0, y: float = 0, id: int = 4):
        self._color = Color(100, 100, 100, 255)
        self.color.randomize_by_range(10)
        self._pos = Vector2(x, y)
        self._id = id
        self._density = 2.5

    @property
    def color(self) -> Color:
        return self._color

    @property
    def pos(self) -> Vector2:
        return self._pos

    @property
    def id(self) -> int:
        return self._id

    @property
    def density(self) -> float:
        return self._density

    def set_pos(self, new_pos: Vector2):
        self._pos = new_pos

    def set_color(self, color: Color):
        self._color = color

    def apply_rules(self, grid):
        x, y = self.pos.get_pos()
        grid_height, grid_width = grid.shape

        def is_valid(x: int, y: int) -> bool:
            return 0 <= x < grid_width and 0 <= y < grid_height

        def is_valid_and_empty(x: int, y: int) -> bool:
            return is_valid(x, y) and (grid[y, x] is None or grid[y, x].id == 0)

        # Gravità
        if is_valid_and_empty(x, y + 1):
            self.set_pos(Vector2(x, y + 1))
            return

        # Controllo densità
        if is_valid(x, y + 1) and grid[y + 1, x] is not None and grid[y + 1, x].id != 0:
            other_particle = grid[y + 1, x]
            if self.density > other_particle.density:
                self.set_pos(Vector2(x, y + 1))
                other_particle.set_pos(Vector2(x, y))
                return


class Brick(ParticleI):
    def __init__(self, x: float = 0, y: float = 0, id: int = 5):
        self._color = Color(139, 69, 19, 255)
        self.color.randomize_by_range(10)
        self._pos = Vector2(x, y)
        self._id = id
        self._density = 3.0

    @property
    def color(self) -> Color:
        return self._color

    @property
    def pos(self) -> Vector2:
        return self._pos

    @property
    def id(self) -> int:
        return self._id

    @property
    def density(self) -> float:
        return self._density

    def set_pos(self, new_pos: Vector2):
        self._pos = new_pos

    def set_color(self, color: Color):
        self._color = color

    def apply_rules(self, grid):
        # Non fa niente, e va bene così
        pass
