import pygame
import copy

from colors import *

snake_head_size = 20
snake_part_size = 19

class SnakeHead():
    def __init__(self, background, x=60, y=60):
        self.moves = []
        self.cur_dir = pygame.K_RIGHT
        self.snake_part = pygame.draw.rect(background, BLACK,
            (x, y, snake_head_size, snake_head_size), 2)

def update_snake_head_moves(snake_head, key):
    snake_head.cur_dir = key
    snake_head.moves.append(key)

def check_snake_events(snake_head, event):
    '''
    Check all the player (snake) events that could happen
    '''
    if event.type == pygame.KEYDOWN:
        if snake_head.cur_dir != pygame.K_DOWN and \
            event.key == pygame.K_UP:
            update_snake_head_moves(snake_head, event.key)
        elif snake_head.cur_dir != pygame.K_UP and \
            event.key == pygame.K_DOWN:
            update_snake_head_moves(snake_head, event.key)
        elif snake_head.cur_dir != pygame.K_LEFT and \
            event.key == pygame.K_RIGHT:
            update_snake_head_moves(snake_head, event.key)
        elif snake_head.cur_dir != pygame.K_RIGHT and \
            event.key == pygame.K_LEFT:
            update_snake_head_moves(snake_head, event.key)

def move_snake_head(snake_head, direction):
    if direction == pygame.K_LEFT:
        snake_head.snake_part.move_ip(-snake_head_size, 0)
    elif direction == pygame.K_RIGHT:
        snake_head.snake_part.move_ip(snake_head_size, 0)
    elif direction == pygame.K_DOWN:
        snake_head.snake_part.move_ip(0, snake_head_size)
    elif direction == pygame.K_UP:
        snake_head.snake_part.move_ip(0, -snake_head_size)

def update_snake_head(snake_head, background):
    '''
    Update the state of the snake
    '''
    # Just move the snake in the current direction if there are no moves
    # Otherwise excute the first move on the list and remove it
    if len(snake_head.moves) == 0:
        move_snake_head(snake_head, snake_head.cur_dir)
    else:
        move_snake_head(snake_head, snake_head.moves[0])
        snake_head.moves.remove(snake_head.moves[0])

    # Draw the position
    pygame.draw.rect(background, BLACK,
        snake_head.snake_part, 2)

class SnakeBody():
    def __init__(self, background, x, y, on_screen=False, next_part=None):
        self.on_screen = on_screen
        self.snake_part = pygame.draw.rect(background, BLACK,
            (x, y, snake_part_size, snake_part_size), 2)
        self.next_part = next_part

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
