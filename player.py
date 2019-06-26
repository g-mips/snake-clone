import pygame

from colors import *

class Player():
    def __init__(self, background, x=50, y=50):
        self.cur_dir = pygame.K_RIGHT

        self.snake = pygame.draw.rect(background, BLACK,
            (x, y, 20, 20), 2)

def check_snake_events(plyr, event):
    '''
    Check all the player (snake) events that could happen
    '''
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            plyr.cur_dir = event.key
        elif event.key == pygame.K_DOWN:
            plyr.cur_dir = event.key
        elif event.key == pygame.K_RIGHT:
            plyr.cur_dir = event.key
        elif event.key == pygame.K_LEFT:
            plyr.cur_dir = event.key

def update_snake(plyr, background):
    '''
    Update the state of the snake
    '''
    if plyr.cur_dir == pygame.K_LEFT:
        plyr.snake.move_ip(-1, 0)
    elif plyr.cur_dir == pygame.K_RIGHT:
        plyr.snake.move_ip(1, 0)
    elif plyr.cur_dir == pygame.K_DOWN:
        plyr.snake.move_ip(0, 1)
    elif plyr.cur_dir == pygame.K_UP:
        plyr.snake.move_ip(0, -1)

    pygame.draw.rect(background, BLACK,
        plyr.snake, 2)
