import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        x = self.left
        y = self.top
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size), 1)
                x += self.cell_size
            y += self.cell_size
            x = self.left

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        if mouse_pos[0] < self.left or \
                mouse_pos[0] > self.left + self.cell_size * self.width or mouse_pos[1] < self.top or \
                mouse_pos[1] > self.top + self.cell_size * self.height:
            return None
        helper = list(mouse_pos)
        helper = [i // self.cell_size for i in helper]
        return tuple(helper)

    def on_click(self, cell):
        print(cell if cell else None)
