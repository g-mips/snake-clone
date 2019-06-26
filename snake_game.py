import pygame
import sys
import getopt

import player

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
    clock = pygame.time.Clock()
    FPS = 60

    main_screen = pygame.display.set_mode((width, height))
    plyr = player.Player(main_screen) #player.setup_snake(main_screen)

    running = True
    playtime = 0.0
    while running:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0

        text = "FPS: {0:.2f} Playtime: {1:.2f}".format(
            clock.get_fps(), playtime)
        pygame.display.set_caption(text)

        if not event_handler(plyr):
            running = False

        main_screen.fill((255, 255, 255))

        player.update_snake(plyr, main_screen)
        pygame.display.update()

    pygame.quit()

def usage():
    print('{} [-W <width>] [-H <height>]'.format(sys.argv[0]))

if __name__ == "__main__":
    width = 640
    height = 480

    if len(sys.argv) != 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hW:H:", ["help", "width=", "height="])
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

    main(width, height)
