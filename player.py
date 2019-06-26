import pygame

current_direction = pygame.K_RIGHT

def check_snake_events(event):
    '''
    Check all the player (snake) events that could happen
    '''
    global current_direction

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            current_direction = event.key
        elif event.key == pygame.K_DOWN:
            current_direction = event.key
        elif event.key == pygame.K_RIGHT:
            current_direction = event.key
        elif event.key == pygame.K_LEFT:
            current_direction = event.key

def setup_snake(background):
    '''
    Setup the initial state of the player (snake)
    '''
    global current_direction

    initial_x = 50
    initial_y = 50

    return pygame.draw.rect(background, (0, 0, 0),
            (initial_x, initial_y, 20, 20), 2)

def update_snake(snake, background):
    global player_keys

    if current_direction == pygame.K_LEFT:
        snake.move_ip(-1, 0)
    elif current_direction == pygame.K_RIGHT:
        snake.move_ip(1, 0)
    elif current_direction == pygame.K_DOWN:
        snake.move_ip(0, 1)
    elif current_direction == pygame.K_UP:
        snake.move_ip(0, -1)

    pygame.draw.rect(background, (0, 0, 0),
            snake, 2)
