import pygame
import sys
import getopt
import random
import copy

from colors import *
import player

border_dist = 5

def setup_borders(background):
    '''
    This returns an array of lines. Each line is setup separately because
    collision detection doesn't work properly as the player is always in
    the "rect" otherwise.
    '''
    width, height = background.get_size()

    line_1_start = (border_dist, border_dist)
    line_2_start = (border_dist, height - border_dist)
    line_3_start = (width - border_dist, height - border_dist)
    line_4_start = (width - border_dist, border_dist)

    return [pygame.draw.line(background, BLACK, line_1_start, line_2_start, 5),
        pygame.draw.line(background, BLACK, line_2_start, line_3_start, 5),
        pygame.draw.line(background, BLACK, line_3_start, line_4_start, 5),
        pygame.draw.line(background, BLACK, line_4_start, line_1_start, 5)]

def create_random_prize(background):
    '''
    Create a prize in a random spot within the background given
    '''
    width, height = background.get_size()

    prize_width = 20
    prize_height = 20
    x = random.randrange(border_dist + 1,
        width - (border_dist + 1) - prize_width)
    y = random.randrange(border_dist + 1,
        height - (border_dist + 1) - prize_width)

    return pygame.draw.rect(background, RED,
        (x, y, prize_width, prize_height), 2)

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

def create_surface(size, red, green, blue):
    '''
    Create a surface in an initial state
    '''
    surface = pygame.Surface(size)
    surface.fill((red, green, blue))

    return surface.convert()

def main(width, height):
    pygame.init()

    # Setup clock
    clock = pygame.time.Clock()
    FPS = 10

    # Setup screen and objects
    main_screen = pygame.display.set_mode((width, height))
    snake_head = player.SnakeHead(main_screen)
    borders = setup_borders(main_screen)
    prize = create_random_prize(main_screen)

    # Main loop
    running = True
    playtime = 0.0
    snake_parts = []
    while running:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0

        # Debug info
        text = "FPS: {0:.2f} Playtime: {1:.2f}".format(
            clock.get_fps(), playtime)
        pygame.display.set_caption(text)

        # Run through all the events
        running = event_handler(snake_head)

        if running:
            # Clear the screen
            main_screen.fill(WHITE)

            # Update the snake head
            player.update_snake_head(snake_head, main_screen)

            # Update the snake body
            prev_snake = snake_head.snake_part
            for snake_part in snake_parts:
                player.update_snake_body(snake_part, prev_snake, main_screen)
                prev_snake = snake_part.snake_part

            # Draw the borders
            borders = setup_borders(main_screen)

            # Draw the prize
            pygame.draw.rect(main_screen, RED, prize, 2)

            # Update the screen
            pygame.display.update()

            # Test to see if the snake ran into a border
            for border in borders:
                if snake_head.snake_part.colliderect(border):
                    running = False
                    break

            # Test to see if the snake head ran into the snake body
            if running:
                for snake_part in snake_parts:
                    if snake_part.on_screen and \
                        snake_head.snake_part.colliderect(
                            snake_part.snake_part):
                        running = False
                        break

            # Test to see if the snake head collected a prize
            if running and snake_head.snake_part.colliderect(prize):
                prize = create_random_prize(main_screen)
                x = snake_head.snake_part.x
                y = snake_head.snake_part.y

                if len(snake_parts) > 0:
                    x = snake_parts[len(snake_parts) - 1].snake_part.x
                    y = snake_parts[len(snake_parts) - 1].snake_part.y

                snake_parts.append(player.SnakeBody(main_screen, x, y))

    pygame.quit()

def usage():
    print('{} [-W <width>] [-H <height>]'.format(sys.argv[0]))

if __name__ == "__main__":
    width = 640
    height = 480

    if len(sys.argv) != 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hW:H:",
                ["help", "width=", "height="])
        except getopt.GetoptError:
            usage()
            sys.exit(1)

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit()
            elif opt in ('-W', '--width'):
                width = arg
            elif opt in ('-H', '--height'):
                height = arg

    random.seed()

    main(width, height)
