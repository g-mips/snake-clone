import pygame
import sys
import getopt
import random
import copy

from colors import *
import player

prize_size = player.snake_part_size

border_dist = 5
debug = False

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

    # Setup clock
    clock = pygame.time.Clock()
    FPS = 10

    # Setup screens
    main_screen = pygame.display.set_mode((width, height))
    level_width = width - (border_dist * 2) - 2
    level_height = height - (border_dist * 2) - 2
    level = create_surface((level_width, level_height), WHITE)

    # Setup snake
    snake_head = player.SnakeHead(level)
    snake_head_part = pygame.Rect(
        snake_head.snake_part.x + 1, snake_head.snake_part.y + 1,
        player.snake_part_size, player.snake_part_size)
    snake_parts = [ player.SnakeBody(level,
        snake_head_part.x - player.snake_head_size - 1, 60,
        True, snake_head_part) ]
    snake_parts.append(player.SnakeBody(level,
        snake_head_part.x - (player.snake_head_size * 2) - 1, 60,
        True, snake_parts[0].snake_part))

    # Setup Prize
    prize = create_random_prize(level)

    # Setup Border
    setup_borders(level)

    # Display level on main screen
    main_screen.blit(level, (border_dist + 2, border_dist + 2))

    # Main loop
    running = True
    playtime = 0.0

    while running:
        milliseconds = clock.tick(FPS)

        # Debug info
        if debug:
            playtime += milliseconds / 1000.0
            text = "FPS: {0:.2f} Playtime: {1:.2f}".format(
                    clock.get_fps(), playtime)
            pygame.display.set_caption(text)

        # Run through all the events
        running = event_handler(snake_head)
        if running:
            # Clear the screen
            main_screen.fill(WHITE)
            level.fill(WHITE)

            if debug:
                show_grid(level)

            # Update the snake head
            player.update_snake_head(snake_head, level)

            # Update the snake body
            prev_snake = pygame.Rect(
                    snake_head.snake_part.x + 1, snake_head.snake_part.y + 1,
                    player.snake_part_size, player.snake_part_size)
            for snake_part in snake_parts:
                player.update_snake_body(snake_part, prev_snake, level)
                prev_snake = snake_part.snake_part

            # Draw the prize
            pygame.draw.rect(level, RED, prize, 2)

            # Draw the borders
            setup_borders(level)

            # Update the screens
            main_screen.blit(level, (border_dist + 2, border_dist + 2))
            pygame.display.update()

            # Test to see if the snake ran into a border
            if snake_head.snake_part.x < 0 or \
                (snake_head.snake_part.x +
                 snake_head.snake_part.width) > level_width or \
                snake_head.snake_part.y < 0 or \
                (snake_head.snake_part.y +
                 snake_head.snake_part.height) > level_height:
                running = False

            # Test to see if the snake head ran into the snake body
            if running:
                for snake_part in snake_parts:
                    if snake_part.on_screen and \
                        snake_head.snake_part.colliderect(
                            snake_part.snake_part):
                        print('snake part')
                        running = False
                        break

            # Test to see if the snake head collected a prize
            if running and snake_head.snake_part.colliderect(prize):
                prize = create_random_prize(level)
                x = snake_head.snake_part.x
                y = snake_head.snake_part.y

                if len(snake_parts) > 0:
                    x = snake_parts[len(snake_parts) - 1].snake_part.x
                    y = snake_parts[len(snake_parts) - 1].snake_part.y
                else:
                    if snake_head.cur_dir == pygame.K_LEFT:
                        x += 1
                    elif snake_head.cur_dir == pygame.K_RIGHT:
                        x -= 1
                    elif snake_head.cur_dir == pygame.K_DOWN:
                        y -= 1
                    elif snake_head.cur_dir == pygame.K_UP:
                        y += 1

                snake_parts.append(player.SnakeBody(main_screen, x, y))

    pygame.quit()

def usage():
    print('{} [-W <width>] [-H <height>]'.format(sys.argv[0]))

if __name__ == "__main__":
    width = 655
    height = 495

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
            elif opt in ('-W', '--width'):
                width = arg
            elif opt in ('-H', '--height'):
                height = arg

    random.seed()

    main(width, height)
