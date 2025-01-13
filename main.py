import pygame
import math
import heapq

# Stałe do oznaczania wartości na mapie
FREE = 0
OBSTACLE = 5
PATH = 3
START = 2
GOAL = 4

# Rozmiary ekranu i komórki
CELL_SIZE = 30
WIDTH = 20  # Liczba kolumn
HEIGHT = 20  # Liczba wierszy
SCREEN_WIDTH = WIDTH * CELL_SIZE
SCREEN_HEIGHT = HEIGHT * CELL_SIZE

# Funkcja pomocnicza do obliczania odległości euklidesowej
def heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Implementacja algorytmu A*
def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    open_set_list = []  # Do śledzenia wszystkich otwartych komórek
    closed_set = []  # Do śledzenia wszystkich przetworzonych komórek

    while open_set:
        _, current = heapq.heappop(open_set)

        # Jeśli osiągnięto cel, odtwarzamy ścieżkę
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], open_set_list, closed_set

        closed_set.append(current)

        # Iteracja po sąsiadach
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == OBSTACLE or neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    if neighbor not in open_set_list:
                        open_set_list.append(neighbor)

    # Jeśli ścieżka nie została znaleziona
    return None, open_set_list, closed_set

# Wizualizacja mapy i animacja algorytmu A*
def visualize(grid, path=None, open_set_list=None, closed_set=None):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("A* Algorithm Visualization")
    clock = pygame.time.Clock()

    path_built = False
    draw_open_closed_done = False
    path_index = 0

    screen.fill((255, 255, 255))

    def draw_grid():
        for row in range(HEIGHT):
            for col in range(WIDTH):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if grid[row][col] == OBSTACLE:
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                elif grid[row][col] == PATH:
                    pygame.draw.rect(screen, (0, 255, 0), rect)
                elif grid[row][col] == START:
                    pygame.draw.rect(screen, (128, 0, 128), rect)
                elif grid[row][col] == GOAL:
                    pygame.draw.rect(screen, (255, 255, 0), rect)
                # elif grid[row][col] == FREE:
                #     pygame.draw.rect(screen, (255, 255, 255), rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    def draw_open_closed():
        nonlocal draw_open_closed_done
        for x, y in open_set_list[:-1]:
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 0, 255), rect)  # Niebieskie komórki (otwarte)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Siatka na wierzchu
            pygame.display.flip()
            pygame.time.delay(20)  # Opóźnienie animacji

        for x, y in closed_set[1:]:
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (255, 0, 0), rect)  # Czerwone komórki (zamknięte)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Siatka na wierzchu
            pygame.display.flip()
            pygame.time.delay(20)  # Opóźnienie animacji

        draw_open_closed_done = True

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid()

        # Rysowanie otwartych i zamkniętych komórek
        if not draw_open_closed_done:
            draw_open_closed()

        # Budowanie ścieżki
        if draw_open_closed_done and path and not path_built:
            if path_index < len(path):
                x, y = path[path_index]
                grid[x][y] = PATH
                path_index += 1
                pygame.display.flip()
                pygame.time.delay(50)  # Opóźnienie wyświetlania ścieżki
            else:
                path_built = True

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Ładowanie mapy z pliku
def load_grid_from_file(filename):
    with open(filename, 'r') as file:
        grid = []
        for line in file:
            grid.append(list(map(int, line.split())))
    return grid

# Ładowanie mapy z pliku grid.txt
grid = load_grid_from_file('grid.txt')

# Start i cel
start = (0, 0)
goal = (19, 16)

# Sprawdzenie przeszkód
if grid[start[0]][start[1]] == OBSTACLE or grid[goal[0]][goal[1]] == OBSTACLE:
    print("Start lub cel znajduje się na przeszkodzie!")
else:
    # Oznaczamy start i cel na mapie
    grid[start[0]][start[1]] = START
    grid[goal[0]][goal[1]] = GOAL

    # Szukanie ścieżki za pomocą A*
    path, open_set_list, closed_set = a_star(grid, start, goal)

    # Jeśli ścieżka została znaleziona, wizualizujemy
    if path:
        visualize(grid, path, open_set_list, closed_set)
    else:
        print("Nie znaleziono ścieżki.")
