from snake import *
from os import environ

red = (237, 9, 9)

def draw_screen(surface):
    surface.fill(SURFACE_CLR)

def Your_score(score, score_font, game_surface):
    value = score_font.render("Score: " + str(score), True, red)
    game_surface.blit(value, (0, 0))

def draw_grid(surface):
    x = 0
    y = 0
    for r in range(ROWS):
        x = x + SQUARE_SIZE
        y = y + SQUARE_SIZE
        pygame.draw.line(surface, GRID_CLR, (x, 0), (x, HEIGHT))
        pygame.draw.line(surface, GRID_CLR, (0, y), (WIDTH, y))


def play_game():
    pygame.init()
    fontText = pygame.font.SysFont("bahnschrift", 16)
    fontNumber = pygame.font.SysFont("comicsansms", 15)

    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Snake Game")
    game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake(game_surface)

    
    draw_screen(game_surface)
    draw_grid(game_surface)
    snake.update()
    Your_score(snake.score, fontNumber, game_surface)
    clock.tick(FPS)
    pygame.display.update()

