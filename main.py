import pygame

from sourses.Board import Board

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Сапёр')
    size = width, height = 520, 520
    screen = pygame.display.set_mode(size)
    board = Board(10, 10)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
