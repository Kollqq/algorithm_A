import pygame
import math
import heapq

# Константы для обозначения значений на карте
FREE = 0
OBSTACLE = 5
PATH = 3
START = 2
GOAL = 4

# Размеры экрана и клетки
CELL_SIZE = 30
WIDTH = 20  # Количество столбцов
HEIGHT = 20  # Количество строк
SCREEN_WIDTH = WIDTH * CELL_SIZE
SCREEN_HEIGHT = HEIGHT * CELL_SIZE

# Вспомогательная функция для вычисления евклидовой дистанции
def heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Реализация алгоритма A*
def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    open_set_list = []  # Для отслеживания всех открытых ячеек
    closed_set = []  # Для отслеживания всех обработанных ячеек

    while open_set:
        _, current = heapq.heappop(open_set)

        # Если достигли цели, восстанавливаем путь
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], open_set_list, closed_set

        closed_set.append(current)

        # Перебираем соседей
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

    # Если путь не найден
    return None, open_set_list, closed_set

# Визуализация карты и анимация алгоритма A*
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
            pygame.draw.rect(screen, (0, 0, 255), rect)  # Синие клетки (открытые)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Сетка поверх
            pygame.display.flip()
            pygame.time.delay(20)  # Задержка для анимации

        for x, y in closed_set[1:]:
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (255, 0, 0), rect)  # Красные клетки (закрытые)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Сетка поверх
            pygame.display.flip()
            pygame.time.delay(20)  # Задержка для анимации

        draw_open_closed_done = True

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid()

        # Отрисовка открытых и закрытых клеток
        if not draw_open_closed_done:
            draw_open_closed()

        # Построение пути
        if draw_open_closed_done and path and not path_built:
            if path_index < len(path):
                x, y = path[path_index]
                grid[x][y] = PATH
                path_index += 1
                pygame.display.flip()
                pygame.time.delay(50)  # Задержка для отображения пути
            else:
                path_built = True

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Загрузка карты из файла
def load_grid_from_file(filename):
    with open(filename, 'r') as file:
        grid = []
        for line in file:
            grid.append(list(map(int, line.split())))
    return grid

# Загрузка карты из файла grid.txt
grid = load_grid_from_file('grid.txt')

# Старт и цель
start = (0, 0)
goal = (19, 16)

# Проверка на барьеры
if grid[start[0]][start[1]] == OBSTACLE or grid[goal[0]][goal[1]] == OBSTACLE:
    print("Старт или цель находятся на препятствии!")
else:
    # Отметим старт и цель на карте
    grid[start[0]][start[1]] = START
    grid[goal[0]][goal[1]] = GOAL

    # Поиск пути с использованием A*
    path, open_set_list, closed_set = a_star(grid, start, goal)

    # Если путь найден, визуализируем
    if path:
        visualize(grid, path, open_set_list, closed_set)
    else:
        print("Путь не найден.")
