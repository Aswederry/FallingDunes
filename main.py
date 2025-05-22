import pygame
from Particles import *
from Quadtree import QuadNode


# Precalcolo offset cerchio per spawn, senno lagga troppo, assurdo comunque dover fare certe cose perchè python è così... :p
def get_circle_offsets(radius):
    offsets = []
    for y in range(-radius, radius + 1):
        for x in range(-radius, radius + 1):
            if x ** 2 + y ** 2 <= radius ** 2:
                offsets.append((x, y))
    return np.array(offsets, dtype=np.int32)


def create_particle(particle_class, x, y, id_map):
    return particle_class(x, y, id_map[particle_class])


def spawn_particle(pos: Vector2, particle: ParticleI, grid, quadtree, radius: int = 5):
    x_center, y_center = map(int, pos.get_pos())
    grid_height, grid_width = grid.shape
    offsets = get_circle_offsets(radius)
    id_map = {Sand: 1, Water: 2, Steam: 3, Stone: 4, Brick: 5}

    positions = offsets + np.array([x_center, y_center])
    valid_mask = (
            (0 <= positions[:, 0]) & (positions[:, 0] < grid_width) &
            (0 <= positions[:, 1]) & (positions[:, 1] < grid_height)
    )
    valid_positions = positions[valid_mask]

    for x, y in valid_positions:
        if grid[y, x] is None:
            new_particle = create_particle(particle.__class__, x, y, id_map)
            grid[y, x] = new_particle
            quadtree.insert(x, y, grid_width, grid_height)


def update_grid(grid, quadtree):
    grid_height, grid_width = grid.shape
    particles = quadtree.get_active_particles(grid)
    particles.sort(key=lambda p: p[2], reverse=True)

    new_quadtree = QuadNode(0, 0, grid_width, grid_height, 0, quadtree.max_depth)
    for particle, x, y in particles:
        grid[y, x] = None
        particle.apply_rules(grid)
        new_x, new_y = map(int, particle.pos.get_pos())
        if 0 <= new_x < grid_width and 0 <= new_y < grid_height:
            grid[new_y, new_x] = particle
            new_quadtree.insert(new_x, new_y, grid_width, grid_height)

    return new_quadtree


def render_grid(grid, screen, cell_size, quadtree):
    screen.fill((255, 255, 255))  # La pulizia dello schermo viene fatta qua, anche se non cambia niente
    for particle, x, y in quadtree.get_active_particles(grid):
        if particle is not None and isinstance(particle, ParticleI):
            color = particle.color.get_color_rgb()
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))


def select_particle():
    global selected_particle
    keys = pygame.key.get_pressed()
    particle_map = {
        pygame.K_1: Sand,
        pygame.K_2: Water,
        pygame.K_3: Steam,
        pygame.K_4: Stone,
        pygame.K_5: Brick
    }
    for key, particle in particle_map.items():
        if keys[key]:
            selected_particle = particle
            print(selected_particle)
            break


def reset():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        grid.fill(None)
        quadtree.clear()


def update_text():
    font = pygame.font.SysFont("monospace", 15)
    selectedLabel = font.render(selected_particle.__name__, 1, (0, 0, 0))
    screen.blit(selectedLabel, (0, 0))

    radiusLabel = font.render(f"Raggio: {radius}", 1, (0, 0, 0))
    screen.blit(radiusLabel, (0, 10))


# Configurazione
grid_length = 64
grid_height = 64
cell_size = 12
max_depth = 4  # Numero massimo di suddivisioni per il quadtree
grid = np.full((grid_height, grid_length), None, dtype=object)
quadtree = QuadNode(0, 0, grid_length, grid_height, 0, max_depth)
selected_particle = Sand
radius = 5


pygame.init()
screen = pygame.display.set_mode((grid_length * cell_size, grid_height * cell_size))
pygame.display.set_caption("Falling Dunes")
clock = pygame.time.Clock()
running = True

# Ciclo principale
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]):
            if selected_particle is not None:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = mouse_x // cell_size, mouse_y // cell_size
                if 0 <= grid_x < grid.shape[1] and 0 <= grid_y < grid.shape[0]:
                    spawn_particle(Vector2(grid_x, grid_y), selected_particle(grid_x, grid_y), grid, quadtree, radius)

        if event.type == pygame.MOUSEWHEEL:
            radius += event.y  # Aumenta con rotella su, diminuisce con rotella giù
            radius = max(1, min(radius, 20))
            print(f"Raggio spawn: {radius}")

    # Operazioni sulla griglia
    quadtree = update_grid(grid, quadtree)

    # Rendering
    render_grid(grid, screen, cell_size, quadtree)
    update_text()

    # Input
    select_particle()
    reset()

    # Altra roba di pygame
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
