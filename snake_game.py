import pygame
import sys
import getopt
import random

from colors import *
import player

def setup_borders(background):
    '''
    This returns an array of lines. Each line is setup separately because
    collision detection doesn't work properly as the player is always in
    the "rect" otherwise.
    '''
    width, height = background.get_size()

    line_1_start = (5, 5)
    line_2_start = (5, height - 5)
    line_3_start = (width - 5, height - 5)
    line_4_start = (width - 5, 5)

    return [pygame.draw.line(background, WHITE, line_1_start, line_2_start, 5),
        pygame.draw.line(background, WHITE, line_2_start, line_3_start, 5),
        pygame.draw.line(background, WHITE, line_3_start, line_4_start, 5),
        pygame.draw.line(background, WHITE, line_4_start, line_1_start, 5)]

def create_random_prize(background):
    width, height = background.get_size()

    x = random.randrange(6, width - 6 - 20)
    y = random.randrange(6, height - 6 - 20)

    return pygame.draw.rect(background, WHITE, (x, y, 20, 20), 2)

def setup_initial_screen(width, height):
    '''
    Create the initial screen
    '''
    screen = pygame.display.set_mode((width, height))

    return screen

def event_handler(plyr):
    '''
    Handles events. Returns 'False' if an end the game event occurred
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

        player.check_snake_events(plyr, event)

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
    FPS = 120

    # Setup screen and objects
    main_screen = pygame.display.set_mode((width, height))
    plyr = player.Player(main_screen)
    borders = setup_borders(main_screen)
    prize = create_random_prize(main_screen)

    # Main loop
    running = True
    playtime = 0.0
    while running:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0

        # Debug info
        text = "FPS: {0:.2f} Playtime: {1:.2f}".format(
            clock.get_fps(), playtime)
        pygame.display.set_caption(text)

        # Run through all the events
        running = event_handler(plyr)

        # Update the screen
        main_screen.fill(BLACK)

        player.update_snake(plyr, main_screen)
        borders = setup_borders(main_screen)
        pygame.draw.rect(main_screen, WHITE, prize, 2)
        pygame.display.update()

        # Test to see if the snake ran into a border
        for border in borders:
            if plyr.snake.colliderect(border):
                running = False
                break

        if plyr.snake.colliderect(prize):
            prize = create_random_prize(main_screen)

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
