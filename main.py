from random import choices


class MineSweeper:
    def __init__(self, dimension=3, mines=1):
        # Сделан первый ход
        self.used = False
        self.mines = mines
        # Множество кортежей с координатами бомб
        self.memo = None
        self.dim = dimension
        # Осталось открыть клеток
        self.cells = self.dim ** 2
        self.field = [[0] * self.dim for _ in range(self.dim)]

    # "Обнуление" поля
    def clear(self):
        self.field = [[0] * self.dim for _ in range(self.dim)]
        self.used = False
        self.cells = self.dim ** 2

    # Размещение мин на поле
    def create(self):
        self.clear()
        x = choices(range(self.dim), k=self.mines)
        y = choices(range(self.dim), k=self.mines)
        s = set(zip(x, y))
        while len(s) != self.mines:
            x = choices(range(self.dim), k=self.mines)
            y = choices(range(self.dim), k=self.mines)
            s = set(zip(x, y))
        self.memo = s
        for i in self.memo:
            self.field[i[0]][i[1]] = 9

    # Количество бомб вохруг клетки (х:у)
    def num_of_bombs(self, x, y):
        nob = 0
        for i in set(range(x - 1, x + 2)).intersection(set(range(self.dim))):
            for j in set(range(y - 1, y + 2)).intersection(set(range(self.dim))):
                if (i, j) in self.memo:
                    nob += 1
        return nob

    # Обход в ширину от клетки (х:у)
    def quantity(self, x, y):
        if self.field[x][y] == 0:
            nob = self.num_of_bombs(x, y)
            if nob == 0:
                self.field[x][y] = 14
                for i in set(range(x - 1, x + 2)).intersection(set(range(self.dim))):
                    for j in set(range(y - 1, y + 2)).intersection(set(range(self.dim))):
                        if i == x and j == y:
                            continue
                        if self.field[i][j] == 0:
                            nob_ij = self.num_of_bombs(i, j)
                            if nob_ij:
                                self.field[i][j] = nob_ij
                                self.cells -= 1
                            else:
                                self.quantity(i, j)
                self.field[x][y] = 13
            else:
                self.field[x][y] = nob
            self.cells -= 1

    def dig(self, x, y, act=None):
        if act:
            act = act.upper()
        if act == 'B' and self.field[x][y] in (0, 9, 12):
            self.field[x][y] = 10
            if (x, y) in self.memo:
                self.cells -= 1
        elif act == 'Q' and self.field[x][y] in (0, 9, 12):
            if self.field[x][y] == 10 and (x, y) in self.memo:
                self.cells += 1
            self.field[x][y] = 12
        elif act == 'C' and (self.field[x][y] == 12 or self.field[x][y] == 10):
            if self.field[x][y] == 10 and (x, y) in self.memo:
                self.cells += 1
            if (x, y) not in self.memo:
                self.field[x][y] = 0
            else:
                self.field[x][y] = 9
        else:
            if self.used:
                if self.field[x][y] == 9:
                    self.field[x][y] = 15
                    return
                elif self.field[x][y] == 13:
                    return
                else:
                    self.quantity(x, y)
            else:
                while self.field[x][y] == 9:
                    self.clear()
                    self.create()
                self.used = True
                self.quantity(x, y)

    def print_board(self):
        print("    ", end="")
        for i in range(1, self.dim + 1):
            ln = len(str(i))
            if ln == 1:
                print(f" {i} ", end='')
            elif ln == 2:
                print(f" {i}", end='')
            else:
                print(i, end='')
        print('\n' + '    ' + '---' * self.dim)
        for i in range(self.dim):
            print(str(i + 1).rjust(2, ' ') + '| ', end='')
            for j in range(self.dim):
                if self.field[i][j] % 9 == 0:
                    print('[ ]', end='')
                elif self.field[i][j] == 10:
                    print('[F]', end='')
                elif 0 < self.field[i][j] < 9:
                    print(f" {self.field[i][j]} ", end='')
                elif self.field[i][j] == 13:
                    print('   ', end='')
                elif self.field[i][j] == 12:
                    print('[?]', end='')
                elif self.field[i][j] == 15:
                    print('[@]', end='')
            print()
        print(self.cells)

    def show_mines(self):
        print("    ", end="")
        for i in range(1, self.dim + 1):
            ln = len(str(i))
            if ln == 1:
                print(f" {i} ", end='')
            elif ln == 2:
                print(f" {i}", end='')
            else:
                print(i, end='')
        print('\n' + '    ' + '---' * self.dim)
        for i in range(self.dim):
            print(str(i + 1).rjust(2, ' ') + '| ', end='')
            for j in range(self.dim):
                if self.field[i][j] == 0:
                    print('[ ]', end='')
                if self.field[i][j] == 9:
                    print('[*]', end='')
                elif self.field[i][j] == 10:
                    print('[F]', end='')
                elif 0 < self.field[i][j] < 9:
                    print(f" {self.field[i][j]} ", end='')
                elif self.field[i][j] == 13:
                    print('   ', end='')
                elif self.field[i][j] == 12:
                    print('[?]', end='')
                elif self.field[i][j] == 15:
                    print('[@]', end='')
            print()


ms = MineSweeper(3, 1)
ms.create()
ms.print_board()
while True:
    print('Возможные действия:\n'
          'B - отметить бомбу\n'
          'Q - подозрение на бомбу\n'
          'C - снять отметку\n'
          'Без действия - копать\n'
          'Введите х, у и возможное действие:')
    x, y, *action = input().split()
    action = ''.join(action)
    x = int(x) - 1
    y = int(y) - 1
    ms.dig(x, y, action)
    ms.print_board()
    if ms.cells == 0:
        print('\n----------------- You are WIN !!! ------------------')
        break
    if ms.field[x][y] == 15:
        print('\n----------------- BooM !!! ------------------')
        break
