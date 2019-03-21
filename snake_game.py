import pygame

def setup_initial_screen(width, height):
    screen = pygame.display.set_mode((width, height))

    return screen

def event_handler():
    '''
    Handles events. Returns 'False' if an end the game event occurred
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

    return True

def create_surface(size, red, green, blue):
    surface = pygame.Surface(size)
    surface.fill((red, green, blue))
    surface = surface.convert()
    return surface

def main():
    pygame.init()
    clock = pygame.time.Clock()

    width = 640
    height = 480

    screen = setup_initial_screen(width, height)

    background = create_surface(screen.get_size(), 255, 0, 0)
    foreground = create_surface(screen.get_size(), 0, 255, 0)
    screen.blit(background, (0, 0))
    screen.blit(foreground, (0, height/2))

    running = True
    FPS = 60
    playtime = 0.0
    while running:
        milliseconds = clock.tick(FPS)
        playtime += milliseconds / 1000.0
        if not event_handler():
            running = False

        text = "FPS: {0:.2f} Playtime: {1:.2f}".format(clock.get_fps(), playtime)
        pygame.display.set_caption(text)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
