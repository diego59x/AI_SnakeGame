import pygame
from settings import *
from copy import deepcopy
from random import randrange
from square import Square

class Snake:
    def __init__(self, surface):
        self.surface = surface
        self.muerto = False
        self.pos_inicial = [[ROWS // 2 + i, ROWS // 2] for i in range(INITIAL_SNAKE_LENGTH)]
        self.turnos = {}
        self.dir = [-1, 0]
        self.score = 0
        self.movimientos_sin_comer = 0
        self.manzana = Square([randrange(ROWS), randrange(ROWS)], self.surface, es_manzana=True)

        self.cuadros = []
        for pos in self.pos_inicial:
            self.cuadros.append(Square(pos, self.surface))

        self.cabeza = self.cuadros[0]
        self.cola = self.cuadros[-1]
        self.cola.es_cola = True

        self.path = []
        self.is_virtual_snake = False
        self.total_movimientos = 0
        self.won_game = False

    def draw(self):
        self.manzana.draw(APPLE_CLR)
        self.cabeza.draw(HEAD_CLR)
        for sqr in self.cuadros[1:]:
            if self.is_virtual_snake:
                sqr.draw(VIRTUAL_SNAKE_CLR)
            else:
                sqr.draw()

    def set_direccion(self, direccion):
        if direccion == 'left':
            if not self.dir == [1, 0]:
                self.dir = [-1, 0]
                self.turnos[self.cabeza.pos[0], self.cabeza.pos[1]] = self.dir
        if direccion == "right":
            if not self.dir == [-1, 0]:
                self.dir = [1, 0]
                self.turnos[self.cabeza.pos[0], self.cabeza.pos[1]] = self.dir
        if direccion == "up":
            if not self.dir == [0, 1]:
                self.dir = [0, -1]
                self.turnos[self.cabeza.pos[0], self.cabeza.pos[1]] = self.dir
        if direccion == "down":
            if not self.dir == [0, -1]:
                self.dir = [0, 1]
                self.turnos[self.cabeza.pos[0], self.cabeza.pos[1]] = self.dir

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def mover(self):
        for j, sqr in enumerate(self.cuadros):
            p = (sqr.pos[0], sqr.pos[1])
            if p in self.turnos:
                turn = self.turnos[p]
                sqr.mover([turn[0], turn[1]])
                if j == len(self.cuadros) - 1:
                    self.turnos.pop(p)
            else:
                sqr.mover(sqr.dir)
        self.movimientos_sin_comer += 1

    def agregar_casilla(self):
        self.cuadros[-1].es_cola = False
        cola = self.cuadros[-1]  # Cola antes de agregar un nuevo cuadro

        direccion = cola.dir
        if direccion == [1, 0]:
            self.cuadros.append(Square([cola.pos[0] - 1, cola.pos[1]], self.surface))
        if direccion == [-1, 0]:
            self.cuadros.append(Square([cola.pos[0] + 1, cola.pos[1]], self.surface))
        if direccion == [0, 1]:
            self.cuadros.append(Square([cola.pos[0], cola.pos[1] - 1], self.surface))
        if direccion == [0, -1]:
            self.cuadros.append(Square([cola.pos[0], cola.pos[1] + 1], self.surface))

        self.cuadros[-1].dir = direccion
        self.cuadros[-1].es_cola = True  # Cola despues de agregar un nuevo cuadro

    def reset(self):
        self.__init__(self.surface)

    def choque_propio(self):
        for sqr in self.cuadros[1:]:
            if sqr.pos == self.cabeza.pos:
                return True

    def generar_manzana(self):
        self.manzana = Square([randrange(ROWS), randrange(ROWS)], self.surface, es_manzana=True)
        if not self.esta_libre(self.manzana.pos):
            self.generar_manzana()

    def comer_manzana(self):
        if self.cabeza.pos == self.manzana.pos and not self.is_virtual_snake and not self.won_game:
            self.generar_manzana()
            self.movimientos_sin_comer = 0
            self.score += 1
            return True

    def dirigirse(self, position):  
        if self.cabeza.pos[0] - 1 == position[0]:
            self.set_direccion('left')
        if self.cabeza.pos[0] + 1 == position[0]:
            self.set_direccion('right')
        if self.cabeza.pos[1] - 1 == position[1]:
            self.set_direccion('up')
        if self.cabeza.pos[1] + 1 == position[1]:
            self.set_direccion('down')

    def esta_libre(self, position):
        if position[0] >= ROWS or position[0] < 0 or position[1] >= ROWS or position[1] < 0:
            return False
        for sqr in self.cuadros:
            if sqr.pos == position:
                return False
        return True

    def bfs(self, s, e): 
        q = [s]  
        visitados = {tuple(pos): False for pos in GRID}

        visitados[s] = True

        
        prev = {tuple(pos): None for pos in GRID}

        while q: 
            node = q.pop(0)
            vecinos = ADJACENCY_DICT[node]
            for next_node in vecinos:
                if self.esta_libre(next_node) and not visitados[tuple(next_node)]:
                    q.append(tuple(next_node))
                    visitados[tuple(next_node)] = True
                    prev[tuple(next_node)] = node

        path = list()
        p_node = e  

        start_node_found = False
        while not start_node_found:
            if prev[p_node] is None:
                return []
            p_node = prev[p_node]
            if p_node == s:
                path.append(e)
                return path
            path.insert(0, p_node)

        return []  

    def serpiente_virtual(self):  
        serpiente_v = Snake(self.surface)
        for i in range(len(self.cuadros) - len(serpiente_v.cuadros)):
            serpiente_v.agregar_casilla()

        for i, sqr in enumerate(serpiente_v.cuadros):
            sqr.pos = deepcopy(self.cuadros[i].pos)
            sqr.dir = deepcopy(self.cuadros[i].dir)

        serpiente_v.dir = deepcopy(self.dir)
        serpiente_v.turnos = deepcopy(self.turnos)
        serpiente_v.manzana.pos = deepcopy(self.manzana.pos)
        serpiente_v.manzana.es_manzana = True
        serpiente_v.is_virtual_snake = True

        return serpiente_v

    def camino_cola(self):
        tail_pos = deepcopy(self.cuadros[-1].pos)
        self.cuadros.pop(-1)
        path = self.bfs(tuple(self.cabeza.pos), tuple(tail_pos))
        self.agregar_casilla()
        return path

    def vecinos_disponibles(self, pos):
        vecinos_validos = []
        vecinos = get_neighbors(tuple(pos))
        for n in vecinos:
            if self.esta_libre(n) and self.manzana.pos != n:
                vecinos_validos.append(tuple(n))
        return vecinos_validos

    def camino_largo_cola(self):
        vecinos = self.vecinos_disponibles(self.cabeza.pos)
        path = []
        if vecinos:
            dis = -9999
            for n in vecinos:
                if distance(n, self.cuadros[-1].pos) > dis:
                    serpiente_v = self.serpiente_virtual()
                    serpiente_v.dirigirse(n)
                    serpiente_v.mover()
                    if serpiente_v.comer_manzana():
                        serpiente_v.agregar_casilla()
                    if serpiente_v.camino_cola():
                        path.append(n)
                        dis = distance(n, self.cuadros[-1].pos)
            if path:
                return [path[-1]]

    def movimiento_seguro(self):
        vecinos = self.vecinos_disponibles(self.cabeza.pos)
        path = []
        if vecinos:
            path.append(vecinos[randrange(len(vecinos))])
            serpiente_v = self.serpiente_virtual()
            for mover in path:
                serpiente_v.dirigirse(mover)
                serpiente_v.mover()
            if serpiente_v.camino_cola():
                return path
            else:
                return self.camino_cola()

    def crear_camino(self):
        
        if self.score == SNAKE_MAX_LENGTH - 1 and self.manzana.pos in get_neighbors(self.cabeza.pos):
            mejor_camino = [tuple(self.manzana.pos)]
            return mejor_camino

        serpiente_v = self.serpiente_virtual()

        
        path_1 = serpiente_v.bfs(tuple(serpiente_v.cabeza.pos), tuple(serpiente_v.manzana.pos))

        
        path_2 = []

        if path_1:
            for pos in path_1:
                serpiente_v.dirigirse(pos)
                serpiente_v.mover()

            serpiente_v.agregar_casilla()  
            path_2 = serpiente_v.camino_cola()

       

        if path_2: 
            return path_1  

        if self.camino_largo_cola() and\
                self.score % 2 == 0 and\
                self.movimientos_sin_comer < MAX_MOVES_WITHOUT_EATING / 2:

            return self.camino_largo_cola()

        if self.movimiento_seguro():
            return self.movimiento_seguro()

        if self.camino_cola():
    
            return self.camino_cola()


    def update(self):
        self.handle_events()

        self.path = self.crear_camino()
        if self.path:
            self.dirigirse(self.path[0])

        self.draw()
        self.mover()

        if self.score == ROWS * ROWS - INITIAL_SNAKE_LENGTH:  
            self.won_game = True

            print("Gano el juego despues de un total de {} movimientos"
                  .format(self.total_movimientos))

            pygame.time.wait(1000 * WAIT_SECONDS_AFTER_WIN)
            return 1

        self.total_movimientos += 1

        if self.choque_propio() or self.cabeza.choque_pared():
            self.muerto = True
            self.reset()

        if self.movimientos_sin_comer == MAX_MOVES_WITHOUT_EATING:
            self.muerto = True
            self.reset()

        if self.comer_manzana():
            self.agregar_casilla()
