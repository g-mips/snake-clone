import pygame
import sys
import getopt
import random
import copy

from colors import *
import player
import level
import collision

prize_size = player.snake_part_size

border_dist = 5
debug = False

def create_random_prize(background):
    '''
    Create a prize in a random spot within the background given
    '''
    width, height = background.get_size()

    x = random.randrange(player.snake_head_size + 1,
        width - player.snake_head_size - 1, player.snake_head_size)
    y = random.randrange(player.snake_head_size + 1,
        height - player.snake_head_size - 1, player.snake_head_size)

    return pygame.draw.rect(background, RED,
        (x, y, prize_size, prize_size), 1)

def event_handler(snake_head):
    '''
    Handles events. Returns 'False' if an end the game event occurred
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

        player.check_snake_events(snake_head, event)

    return True

def create_surface(size, color):
    '''
    Create a surface in an initial state
    '''
    surface = pygame.Surface(size)
    surface.fill(color)

    return surface.convert()

def main(width, height):
    pygame.init()

    screen_width = int(width)
    screen_height = int(height)
    if width == 0 or height == 0:
        modes = pygame.display.list_modes()
        for i in range(len(modes)):
            print('#{}: {}'.format(i, modes[i]))
        mode_index_str = input('Please choose a mode: ')

        try:
            mode_index = int(mode_index_str)

            if mode_index >= len(modes) or mode_index < 0:
                raise ValueError('Invalid index')
        except ValueError:
            print('Please choose a valid mode index')
            pygame.quit()
            sys.exit(1)

        print(modes[mode_index])

        screen_width, screen_height = modes[mode_index]

    # Setup clock
    clock = pygame.time.Clock()
    FPS = 10

    # Setup screens
    main_screen = pygame.display.set_mode(
        (screen_width, screen_height))#, pygame.FULLSCREEN)
    level_width = int(screen_width / 2)# width - (border_dist * 2)
    level_height = int(screen_height / 2)# height - (border_dist * 2)
    level_sur = create_surface((level_width, level_height), WHITE)

    # Setup snake
    snake_head = player.SnakeHead(level_sur)
    snake_head_part = pygame.Rect(
        snake_head.snake_part.x + 1, snake_head.snake_part.y + 1,
        player.snake_part_size, player.snake_part_size)
    snake_parts = [ player.SnakeBody(level_sur,
        snake_head_part.x - player.snake_head_size - 1, 60,
        True, snake_head_part) ]
    snake_parts.append(player.SnakeBody(level_sur,
        snake_head_part.x - (player.snake_head_size * 2) - 1, 60,
        True, snake_parts[0].snake_part))

    # Setup Prize
    prize = create_random_prize(level_sur)

    # Setup Border
    level.setup_borders(level_sur)

    # Display level on main screen
    x_loc = int(screen_width / 3)
    y_loc = int(screen_height / 3)
    main_screen.blit(level_sur, (x_loc, y_loc))

    # Main loop
    running = True
    playtime = 0.0

    while running:
        # Run through all the events
        running = event_handler(snake_head)
        if running:
            # Clear the screen
            main_screen.fill(WHITE)

            level.update_level(snake_head, snake_parts, prize, level_sur, debug)

            # Update the screens
            main_screen.blit(level_sur, (x_loc, y_loc))
            pygame.display.update()

            # Collision tests
            if collision.hit_border(snake_head, level_width, level_height) or \
                collision.hit_self(snake_head, snake_parts):
                running = False

            # Test to see if the snake head collected a prize
            if running and snake_head.snake_part.colliderect(prize):
                prize = create_random_prize(level_sur)
                x = snake_head.snake_part.x
                y = snake_head.snake_part.y

                if len(snake_parts) > 0:
                    x = snake_parts[len(snake_parts) - 1].snake_part.x
                    y = snake_parts[len(snake_parts) - 1].snake_part.y

                snake_parts.append(player.SnakeBody(main_screen, x, y))

        milliseconds = clock.tick(FPS)

        # Debug info
        if debug:
            playtime += milliseconds / 1000.0
            text = "FPS: {0:.2f} Playtime: {1:.2f}".format(
                    clock.get_fps(), playtime)
            pygame.display.set_caption(text)

    pygame.quit()

def usage():
    print('{} [-W <width>] [-H <height>]'.format(sys.argv[0]))

if __name__ == "__main__":
    width = 800
    height = 600

    if len(sys.argv) != 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hdW:H:",
                ["help", "debug", "width=", "height="])
        except getopt.GetoptError:
            usage()
            sys.exit(1)

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit()
            elif opt in ('-d', '--debug'):
                debug = True
            #elif opt in ('-W', '--width'):
            #    width = arg
            #elif opt in ('-H', '--height'):
            #    height = arg

    random.seed()

    main(width, height)
