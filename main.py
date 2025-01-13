class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_set = set()

    open_list.append(start_node)

    max_iterations = len(maze) * len(maze[0]) * 10
    iterations = 0

    while len(open_list) > 0:
        iterations += 1
        if iterations > max_iterations:
            print("Błąd: przekroczono limit iteracji. Droga prawdopodobnie jest niedostępna.")
            return None

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_set.add(current_node.position)

        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[0]) - 1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if child.position in closed_set:
                continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            if any(open_node for open_node in open_list if child == open_node and child.g >= open_node.g):
                continue

            open_list.append(child)


def load_maze_from_file(file_name):
    maze = []
    with open(file_name, 'r') as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            maze.append(row)
    return maze


def print_maze(maze):
    for row in maze:
        print(" ".join(str(cell) for cell in row))


def mark_path_on_maze(maze, path):
    for position in path:
        x, y = position
        maze[x][y] = 3


def save_maze_to_file(maze, file_name):
    with open(file_name, 'w') as f:
        for row in maze:
            f.write(" ".join(map(str, row)) + '\n')


def main():
    maze = load_maze_from_file('grid.txt')

    if len(maze) != 20 or len(maze[0]) != 20:
        print("Błąd: mapa musi mieć rozmiar 20x20!")
        return

    start = (0, 0)
    end = (7, 8)

    if maze[start[0]][start[1]] != 0:
        print("Błąd: punkt początkowy znajduje się na przeszkodzie.")
        return

    if maze[end[0]][end[1]] != 0:
        print("Błąd: punkt końcowy znajduje się na przeszkodzie.")
        return

    path = astar(maze, start, end)
    if path:
        mark_path_on_maze(maze, path)
        print("Końcowa mapa z zaznaczoną ścieżką:")
        print_maze(maze)
        save_maze_to_file(maze, 'grid_f.txt')
        print("Końcowa mapa została zapisana w pliku 'grid_f.txt'.")
    else:
        print("Nie znaleziono ścieżki.")


if __name__ == '__main__':
    main()
