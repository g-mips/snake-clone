import pygame

last_direction = pygame.K_LEFT
player_keys = { 'LEFT': False, 'RIGHT': False, 'UP': False, 'DOWN': False }

def check_snake_events(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            last_direction = event.key
            player_keys['UP'] = True
        elif event.key == pygame.K_DOWN:
            last_direction = event.key
            player_keys['DOWN'] = True
        elif event.key == pygame.K_RIGHT:
            last_direction = event.key
            player_keys['RIGHT'] = True
        elif event.key == pygame.K_LEFT:
            last_direction = event.key
            player_keys['LEFT'] = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            player_keys['UP'] = False
        elif event.key == pygame.K_DOWN:
            player_keys['DOWN'] = False
        elif event.key == pygame.K_RIGHT:
            player_keys['RIGHT'] = False
        elif event.key == pygame.K_LEFT:
            player_keys['LEFT'] = False

def setup_snake(background):
    initial_x = 50
    initial_y = 50

    return pygame.draw.rect(background, (0, 0, 0),
            (initial_x, initial_y, 20, 20), 2)

def update_snake(snake, background):
    global player_keys

    if player_keys['UP'] == True:
        snake.move_ip(0, -1)
    if player_keys['DOWN'] == True:
        snake.move_ip(0, 1)
    if player_keys['LEFT'] == True:
        snake.move_ip(-1, 0)
    if player_keys['RIGHT'] == True:
        snake.move_ip(1, 0)

    pygame.draw.rect(background, (0, 0, 0),
            snake, 2)
