import pygame
import time
import random
from utils import *

#BASE CODE EXTRACTED FROM: https://www.edureka.co/blog/snake-game-with-pygame/

pygame.init()
 
pygame.display.set_caption('Proyecto Inteligencia Artificial')
 
time = pygame.time.Clock()

fontText = pygame.font.SysFont("bahnschrift", 16)
fontNumber = pygame.font.SysFont("comicsansms", 25) 
 
snakeTail = 10
speed = 15
 
def SnakeGame():
    game_over = False
    exitGame = False
 
    x1 = width / 2
    y1 = height / 2
 
    x1Direction = 0
    y1Direction = 0
 
    snake_List = []
    SizeSnake = 1
 
    foodPositionX = round(random.randrange(0, width - snakeTail) / 10.0) * 10.0
    foodPositionY = round(random.randrange(0, height - snakeTail) / 10.0) * 10.0
 
    while not game_over:
 
        while exitGame == True:
            dis.fill(black)
            message("C para volver a jugar, Q para salir", white, fontText)
            Your_score(SizeSnake - 1, fontNumber)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        exitGame = False
                    if event.key == pygame.K_c:
                        SnakeGame()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1Direction = -snakeTail
                    y1Direction = 0
                elif event.key == pygame.K_RIGHT:
                    x1Direction = snakeTail
                    y1Direction = 0
                elif event.key == pygame.K_UP:
                    y1Direction = -snakeTail
                    x1Direction = 0
                elif event.key == pygame.K_DOWN:
                    y1Direction = snakeTail
                    x1Direction = 0
 
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            exitGame = True
        x1 += x1Direction
        y1 += y1Direction
        dis.fill(black) # Painting again the screen, this way just appear the real length of the snake
        pygame.draw.rect(dis, green, [foodPositionX, foodPositionY, snakeTail, snakeTail])
        snakeHead = []
        snakeHead.append(x1)
        snakeHead.append(y1)
        snake_List.append(snakeHead)
        if len(snake_List) > SizeSnake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snakeHead:
                exitGame = True
 
        our_snake(snakeTail, snake_List)
        Your_score(SizeSnake - 1, fontNumber)
 
        pygame.display.update()
 
        if x1 == foodPositionX and y1 == foodPositionY:
            foodPositionX = round(random.randrange(0, width - snakeTail) / 10.0) * 10.0
            foodPositionY = round(random.randrange(0, height - snakeTail) / 10.0) * 10.0
            SizeSnake += 1
 
        time.tick(speed)
 
    pygame.quit()
    quit()
 
 
SnakeGame()