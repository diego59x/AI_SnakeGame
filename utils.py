import pygame

def Your_score(score, score_font):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [0, 0])
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])
 
def message(msg, color, font_style):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 16, height / 3])


white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
width = 300
height = 300
 
dis = pygame.display.set_mode((width, height))