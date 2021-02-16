import pygame

WHITE = pygame.Color("white")


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[" "] * width for _ in range(height)]
        self.queue = "cross"
        self.step = 0
        self.coord_ratio = {(0, 0): 0, (0, 1): 1, (0, 2): 2,
                            (1, 0): 3, (1, 1): 4, (1, 2): 5,
                            (2, 0): 6, (2, 1): 7, (2, 2): 8}
        self.win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                 (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                 (0, 4, 8), (2, 4, 6)]
        self.cell_size = 100

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == "X":
                    x_s, y_s = self.cell_size * x, self.cell_size * y
                    start_pos, end_pos = (x_s, y_s), (x_s + self.cell_size, y_s + self.cell_size)
                    pygame.draw.line(screen, WHITE, start_pos, end_pos, 2)
                    start_pos, end_pos = (x_s + self.cell_size, y_s), (x_s, y_s + self.cell_size)
                    pygame.draw.line(screen, WHITE, start_pos, end_pos, 2)
                elif self.board[y][x] == "O":
                    x_s, y_s = self.cell_size * x, self.cell_size * y,
                    r = self.cell_size // 2
                    pygame.draw.circle(screen, WHITE, (x_s + r, y_s + r), r, 2)
                pygame.draw.rect(screen, WHITE, (self.cell_size * x, self.cell_size * y,
                                                 self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        return self.on_click(cell)

    def get_cell(self, mouse_pos):
        return ((mouse_pos[0]) // self.cell_size,
                (mouse_pos[1]) // self.cell_size)

    def on_click(self, cell_coords):
        if self.width > cell_coords[0] >= 0 and self.height > cell_coords[1] >= 0:
            return cell_coords
        else:
            return None

    def draw(self, cell_coords):
        x, y = self.get_click(cell_coords)
        for j in range(self.width):
            for i in range(self.height):
                if j == x and i == y:
                    if self.queue == "cross":
                        if self.board[i][j] and self.board[i][j] != "X":
                            self.board[i][j] = "O"
                            self.queue = "circle"
                    else:
                        if self.board[i][j] and self.board[i][j] != "O":
                            self.board[i][j] = "X"
                            self.queue = "cross"

    # 0 - Ничья, 1 - Победа, 2 - Поражение
    def check_win(self):
        if self.step < 9:
            print(self.board)
        else:
            return 0


if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)
    board = Board(3, 3)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.draw(event.pos)
                board.check_win()
        screen.fill((0, 0, 0))
        board.render()
        pygame.display.flip()
