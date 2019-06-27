import pygame

from colors import *
import player

def show_grid(background):
    '''
    Show a grid based on the snake head size within the border of the
    background
    '''
    width, height = background.get_size()

    for x in range(0, width, player.snake_head_size):
        for y in range(0, height, player.snake_head_size):
            pygame.draw.line(background, GREEN, (0, y), (width, y), 1)
        pygame.draw.line(background, GREEN, (x, 0), (x, height), 1)

def setup_borders(background):
    '''
    This returns an array of lines. Each line is setup separately because
    collision detection doesn't work properly as the player is always in
    the "rect" otherwise.
    '''
    width, height = background.get_size()

    line_1_start = (0, 0)
    line_2_start = (0, height)
    line_3_start = (width, height)
    line_4_start = (width, 0)

    pygame.draw.line(background, BLACK, line_1_start, line_2_start, 5)
    pygame.draw.line(background, BLACK, line_2_start, line_3_start, 5)
    pygame.draw.line(background, BLACK, line_3_start, line_4_start, 5)
    pygame.draw.line(background, BLACK, line_4_start, line_1_start, 5)

def update_level(snake_head, snake_parts, prize, level_sur, debug=False):
    level_sur.fill(WHITE)

    if debug:
        show_grid(level_sur)

    # Update the snake head
    player.update_snake_head(snake_head, level_sur)

    # Update the snake body
    prev_snake = pygame.Rect(
        snake_head.snake_part.x + 1, snake_head.snake_part.y + 1,
        player.snake_part_size, player.snake_part_size)
    for snake_part in snake_parts:
        player.update_snake_body(snake_part, prev_snake, level_sur)
        prev_snake = snake_part.snake_part

    # Draw the prize
    pygame.draw.rect(level_sur, RED, prize, 2)

    # Draw the borders
    setup_borders(level_sur)

def create_level():
    pass

