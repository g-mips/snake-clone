import pygame

class Player():
    def __init__(self, background, x=50, y=50):
        self.cur_dir = pygame.K_RIGHT

        self.snake = setup_snake(background, x, y)

def check_snake_events(player, event):
    '''
    Check all the player (snake) events that could happen
    '''
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            player.cur_dir = event.key
        elif event.key == pygame.K_DOWN:
            player.cur_dir = event.key
        elif event.key == pygame.K_RIGHT:
            player.cur_dir = event.key
        elif event.key == pygame.K_LEFT:
            player.cur_dir = event.key

def setup_snake(background, initial_x, initial_y):
    '''
    Setup the initial state of the player (snake)
    '''
    return pygame.draw.rect(background, (0, 0, 0),
            (initial_x, initial_y, 20, 20), 2)

def update_snake(player, background):
    '''
    Update the state of the snake
    '''
    if player.cur_dir == pygame.K_LEFT:
        player.snake.move_ip(-1, 0)
    elif player.cur_dir == pygame.K_RIGHT:
        player.snake.move_ip(1, 0)
    elif player.cur_dir == pygame.K_DOWN:
        player.snake.move_ip(0, 1)
    elif player.cur_dir == pygame.K_UP:
        player.snake.move_ip(0, -1)

    pygame.draw.rect(background, (0, 0, 0),
            player.snake, 2)
