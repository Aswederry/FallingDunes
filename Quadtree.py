# Modulo quadtree per ottimizare il tutto, ero curioso di sapere come funzionava
# Non so nemmeno che vuol dire metà di sta roba ma funziona quindi sono contento
# A tralaltro aiuta davvero poco per la performance, mi sa che qua il bottleneck è pygame

class QuadNode:
    def __init__(self, x, y, width, height, depth, max_depth):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.depth = depth
        self.max_depth = max_depth
        self.particles = set()  # Coppie (x, y) delle particelle
        self.children = None  # Lista di 4 figli (None se foglia)

    def subdivide(self):
        if self.depth >= self.max_depth:
            return
        half_w, half_h = self.width // 2, self.height // 2
        self.children = [
            QuadNode(self.x, self.y, half_w, half_h, self.depth + 1, self.max_depth),
            QuadNode(self.x + half_w, self.y, self.width - half_w, half_h, self.depth + 1, self.max_depth),
            QuadNode(self.x, self.y + half_h, half_w, self.height - half_h, self.depth + 1, self.max_depth),
            QuadNode(self.x + half_w, self.y + half_h, self.width - half_w, self.height - half_h, self.depth + 1,
                     self.max_depth)
        ]

    def insert(self, x, y, grid_width, grid_height):
        if not (0 <= x < grid_width and 0 <= y < grid_height):
            return
        if self.children:
            idx = (1 if x >= self.x + self.width // 2 else 0) + (2 if y >= self.y + self.height // 2 else 0)
            self.children[idx].insert(x, y, grid_width, grid_height)
        else:
            self.particles.add((x, y))
            if self.depth < self.max_depth and len(self.particles) > 1:
                self.subdivide()
                particles = self.particles.copy()
                self.particles.clear()
                for px, py in particles:
                    self.insert(px, py, grid_width, grid_height)

    def get_active_particles(self, grid):
        if self.children:
            particles = []
            for child in self.children:
                particles.extend(child.get_active_particles(grid))
            return particles
        return [(grid[y, x], x, y) for x, y in self.particles if grid[y, x] is not None]

    def clear(self):
        self.particles.clear()
        if self.children:
            for child in self.children:
                child.clear()
            self.children = None
