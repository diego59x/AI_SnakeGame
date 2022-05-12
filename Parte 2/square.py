import pygame
from settings import *

class Square:
    def __init__(self, pos, surface, es_manzana=False):
        self.pos = pos
        self.surface = surface
        self.es_manzana = es_manzana
        self.es_cola = False
        self.dir = [-1, 0]  # [x, y] direccion

        if self.es_manzana:
            self.dir = [0, 0]

    def draw(self, clr=SNAKE_CLR):
        x, y = self.pos[0], self.pos[1]
        ss, gs = SQUARE_SIZE, GAP_SIZE

        if self.dir == [-1, 0]:
            if self.es_cola:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss, ss - 2*gs))

        if self.dir == [1, 0]:
            if self.es_cola:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss - gs, y * ss + gs, ss, ss - 2*gs))

        if self.dir == [0, 1]:
            if self.es_cola:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss - gs, ss - 2*gs, ss))

        if self.dir == [0, -1]:
            if self.es_cola:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss))

        if self.es_manzana:
            pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))

    def mover(self, direccion):
        self.dir = direccion
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]

    def choque_pared(self):
        if (self.pos[0] <= -1) or (self.pos[0] >= ROWS) or (self.pos[1] <= -1) or (self.pos[1] >= ROWS):
            return True
        else:
            return False