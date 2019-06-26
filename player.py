import pygame
import copy

from colors import *

snake_part_size = 20

class SnakeHead():
    def __init__(self, background, x=50, y=50):
        self.cur_dir = pygame.K_RIGHT
        self.snake_part = pygame.draw.rect(background, BLACK,
            (x, y, snake_part_size, snake_part_size), 2)

def check_snake_events(snake_head, event):
    '''
    Check all the player (snake) events that could happen
    '''
    if event.type == pygame.KEYDOWN:
        if snake_head.cur_dir != pygame.K_DOWN and \
            event.key == pygame.K_UP:
            snake_head.cur_dir = event.key
        elif snake_head.cur_dir != pygame.K_UP and \
            event.key == pygame.K_DOWN:
            snake_head.cur_dir = event.key
        elif snake_head.cur_dir != pygame.K_LEFT and \
            event.key == pygame.K_RIGHT:
            snake_head.cur_dir = event.key
        elif snake_head.cur_dir != pygame.K_RIGHT and \
            event.key == pygame.K_LEFT:
            snake_head.cur_dir = event.key

def update_snake_head(snake_head, background):
    '''
    Update the state of the snake
    '''
    if snake_head.cur_dir == pygame.K_LEFT:
        snake_head.snake_part.move_ip(-(snake_part_size + 1), 0)
    elif snake_head.cur_dir == pygame.K_RIGHT:
        snake_head.snake_part.move_ip(snake_part_size + 1, 0)
    elif snake_head.cur_dir == pygame.K_DOWN:
        snake_head.snake_part.move_ip(0, snake_part_size + 1)
    elif snake_head.cur_dir == pygame.K_UP:
        snake_head.snake_part.move_ip(0, -(snake_part_size + 1))

    pygame.draw.rect(background, BLACK,
        snake_head.snake_part, 2)

class SnakeBody():
    def __init__(self, background, x, y):
        self.on_screen = False
        self.snake_part = pygame.draw.rect(background, BLACK,
            (x, y, snake_part_size, snake_part_size), 2)
        self.next_part = None

def update_snake_body(cur_body, prev_snake_part, background):
    '''
    If the current part is ready to be displayed, display it and save the
    old info
    '''
    if not cur_body.on_screen:
        if not prev_snake_part.colliderect(cur_body.snake_part):
            cur_body.on_screen = True
            cur_body.next_part = copy.deepcopy(prev_snake_part)
            pygame.draw.rect(background, BLACK, cur_body.snake_part, 2)
    else:
        cur_body.snake_part = cur_body.next_part
        cur_body.next_part = copy.deepcopy(prev_snake_part)
        pygame.draw.rect(background, BLACK, cur_body.snake_part, 2)
