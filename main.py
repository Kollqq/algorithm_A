import pygame
import time

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, screen, cell_size):
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = [start_node]
    closed_set = set()

    while open_list:
        current_node = min(open_list, key=lambda n: n.f)
        open_list.remove(current_node)
        closed_set.add(current_node.position)

        if current_node.position == end_node.position:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if not (0 <= node_position[0] < len(maze) and 0 <= node_position[1] < len(maze[0])):
                continue

            if maze[node_position[0]][node_position[1]] == 5:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if child.position in closed_set:
                continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2 + (child.position[1] - end_node.position[1]) ** 2) ** 0.5
            child.f = child.g + child.h

            if any(open_node for open_node in open_list if child == open_node and child.g >= open_node.g):
                continue

            open_list.append(child)

        draw_grid(maze, screen, cell_size, open_list, closed_set)
        time.sleep(0.1)


def draw_grid(maze, screen, cell_size, open_list, closed_set):
    colors = {
        0: (255, 255, 255),
        5: (0, 0, 0),
        3: (0, 255, 0)
    }
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            color = colors[cell] if cell in colors else (200, 200, 200)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    for node in open_list:
        x, y = node.position
        rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (0, 0, 255), rect)

    for position in closed_set:
        x, y = position
        rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (255, 0, 0), rect)

    pygame.display.flip()


def load_maze_from_file(file_name):
    maze = []
    with open(file_name, 'r') as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            maze.append(row)
    return maze


def mark_path_on_maze(maze, path):
    for position in path:
        x, y = position
        maze[x][y] = 3


def main():
    input_file = 'grid.txt'
    output_file = 'grid_f.txt'
    maze = load_maze_from_file(input_file)

    pygame.init()
    cell_size = 30
    width, height = len(maze[0]) * cell_size, len(maze) * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Wizualizacja algorytmu A*")

    start = (0, 0)
    end = (19, 16)

    if maze[start[0]][start[1]] == 5 or maze[end[0]][end[1]] == 5:
        print("Punkt początkowy lub końcowy znajduje się na przeszkodzie.")
        return

    path = astar(maze, start, end, screen, cell_size)

    if path:
        mark_path_on_maze(maze, path)
        draw_grid(maze, screen, cell_size, [], set())
        print("Znaleziono ścieżkę. Zapisuję do pliku.")
        with open(output_file, 'w') as f:
            for row in maze:
                f.write(" ".join(map(str, row)) + '\n')
    else:
        print("Nie znaleziono ścieżki.")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


if __name__ == '__main__':
    main()
