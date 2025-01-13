import pygame

EMPTY, WALL, ROUTE, START_POINT, END_POINT = 0, 5, 3, 2, 4
TILE_SIZE, GRID_DIMENSION = 30, 20

def find_path(grid_map, start_pos, end_pos):
    open_nodes = [start_pos]
    visited = set()
    parent = {}

    while open_nodes:
        current_pos = open_nodes.pop(0)

        if current_pos == end_pos:
            return reconstruct_path(parent, start_pos, end_pos)

        visited.add(current_pos)

        for nx, ny in get_neighbors(grid_map, current_pos):
            if (nx, ny) not in visited and grid_map[nx][ny] != WALL:
                visited.add((nx, ny))
                open_nodes.append((nx, ny))
                parent[(nx, ny)] = current_pos

    return None

def reconstruct_path(parent, start_pos, end_pos):
    path = []
    current_pos = end_pos
    while current_pos != start_pos:
        path.append(current_pos)
        current_pos = parent[current_pos]
    path.append(start_pos)
    return path[::-1]

def get_neighbors(grid_map, position):
    x, y = position
    potential_neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
    return [(nx, ny) for nx, ny in potential_neighbors if 0 <= nx < GRID_DIMENSION and 0 <= ny < GRID_DIMENSION]

def load_map(file_path):
    with open(file_path) as file:
        return [list(map(int, line.split())) for line in file]

def save_map(grid_map, file_path):
    with open(file_path, 'w') as file:
        for row in grid_map:
            file.write(' '.join(map(str, row)) + '\n')

def display_path(grid_map, found_path):
    pygame.init()
    display = pygame.display.set_mode((GRID_DIMENSION * TILE_SIZE, GRID_DIMENSION * TILE_SIZE))
    color_mapping = {EMPTY: (255, 255, 255), WALL: (0, 0, 0), ROUTE: (0, 255, 0), START_POINT: (128, 0, 128), END_POINT: (255, 255, 0)}

    for path_x, path_y in found_path:
        grid_map[path_x][path_y] = ROUTE

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        for row_idx in range(GRID_DIMENSION):
            for col_idx in range(GRID_DIMENSION):
                rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(display, color_mapping.get(grid_map[row_idx][col_idx], (200, 200, 200)), rect)
                pygame.draw.rect(display, (200, 200, 200), rect, 1)

        pygame.display.update()

grid_data = load_map('grid.txt')
start_cell, end_cell = (0, 0), (19, 16)

if grid_data[start_cell[0]][start_cell[1]] == WALL or grid_data[end_cell[0]][end_cell[1]] == WALL:
    print("Początek lub cel znajduje się na przeszkodzie!")
else:
    grid_data[start_cell[0]][start_cell[1]], grid_data[end_cell[0]][end_cell[1]] = START_POINT, END_POINT
    found_path = find_path(grid_data, start_cell, end_cell)
    if found_path:
        display_path(grid_data, found_path)
        save_map(grid_data, 'final_grid.txt')
        print("Końcowa mapa została zapisana w 'final_grid.txt'.")
    else:
        print("Nie znaleziono ścieżki!")
