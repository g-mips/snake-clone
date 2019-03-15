import pygame

def setup_initial_screen(width, height):
    screen = pygame.display.set_mode((width, height))
    background = pygame.Surface(screen.get_size())
    background.fill((255,255,255))
    background = background.convert()

    return screen, background

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

def main():
    pygame.init()
    screen, background = setup_initial_screen(640, 480)

    running = True
    while running:
        if not event_handler():
            running = False
        pygame.display.flip()
        screen.blit(background, (0, 0))

    pygame.quit()

if __name__ == "__main__":
    main()
