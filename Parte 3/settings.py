
WIDTH = 612   
HEIGHT = 612  
ROWS = 17
SQUARE_SIZE = WIDTH // ROWS
GAP_SIZE = 2  

# Colores
SURFACE_CLR = (0, 0, 0)
GRID_CLR = (0, 0, 0)
SNAKE_CLR = (255, 255, 255)
APPLE_CLR = (0, 255, 0)
HEAD_CLR = (255, 255, 255)
VIRTUAL_SNAKE_CLR = (255, 0, 0)


FPS = 30  
INITIAL_SNAKE_LENGTH = 3
WAIT_SECONDS_AFTER_WIN = 15  
MAX_MOVES_WITHOUT_EATING = ROWS * ROWS * ROWS * 2  
SNAKE_MAX_LENGTH = ROWS * ROWS - INITIAL_SNAKE_LENGTH  

# Variables usadis en un algoritmo BFS
GRID = [[i, j] for i in range(ROWS) for j in range(ROWS)]

def get_neighbors(position):
    vecinos = [[position[0] + 1, position[1]],
                 [position[0] - 1, position[1]],
                 [position[0], position[1] + 1],
                 [position[0], position[1] - 1]]
    in_grid_neighbors = []
    for pos in vecinos:
        if pos in GRID:
            in_grid_neighbors.append(pos)
    return in_grid_neighbors


def distance(pos1, pos2):
    x1, x2 = pos1[0], pos2[0]
    y1, y2 = pos1[1], pos2[1]
    return abs(x2 - x1) + abs(y2 - y1)

# Cada posicion es una tupla 
ADJACENCY_DICT = {tuple(pos): get_neighbors(pos) for pos in GRID}
