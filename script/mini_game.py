from constants import *


class Board(pygame.sprite.Sprite):
    def __init__(self, width, height, left, top):
        super().__init__(tic_tae_toe)
        self.width = width
        self.height = height
        self.board = [[" "] * width for _ in range(height)]
        self.step = 0
        self.cell_size = 124
        self.left = left
        self.top = top
        self.cross_image = load_image("player_symbol.png")
        self.zero_image = load_image("irbis_symbol.png")
        self.screen = load_image("mini_game_frame.png")
        self.coord_ratio = {(0, 0): 0, (0, 1): 1, (0, 2): 2,
                            (1, 0): 3, (1, 1): 4, (1, 2): 5,
                            (2, 0): 6, (2, 1): 7, (2, 2): 8}
        self.win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                 (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                 (0, 4, 8), (2, 4, 6)]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                # pygame.draw.rect(self.screen, WHITE, (self.cell_size * x + 33,
                #                                       self.cell_size * y + 119,
                #                                       self.cell_size, self.cell_size), 2)
                if self.board[y][x] == "X":
                    x_figure, y_figure = self.cell_size * x + 33, 119 + self.cell_size * y
                    self.screen.blit(self.cross_image, (x_figure, y_figure))
                elif self.board[y][x] == "O":
                    x_figure, y_figure = self.cell_size * x + 33, 119 + self.cell_size * y
                    self.screen.blit(self.zero_image, (x_figure, y_figure))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        return self.on_click(cell)

    def get_cell(self, mouse_pos):
        return ((mouse_pos[0] - (self.left + 33)) // self.cell_size,
                (mouse_pos[1] - (self.top + 119)) // self.cell_size)

    def on_click(self, cell_coordinates):
        if self.width > cell_coordinates[0] >= 0 and self.height > cell_coordinates[1] >= 0:
            return cell_coordinates
        else:
            pass

    def player_step(self, cell_coords):
        coordinates = self.get_click(cell_coords)
        if coordinates:
            x, y = coordinates
            for j in range(self.width):
                for i in range(self.height):
                    if j == x and i == y:
                        if self.board[i][j] != "X" and self.board[i][j] != "O":
                            self.board[i][j] = "X"
                            self.step += 1
                            return True
                        else:
                            return False
        else:
            pass

    def check_win(self):
        for x in range(self.width):
            for i, coord in enumerate(self.win_combinations):
                y1, x1 = self.get_key(coord[0])
                y2, x2 = self.get_key(coord[1])
                y3, x3 = self.get_key(coord[2])
                if self.board[x1][y1] == self.board[x2][y2] == self.board[x3][y3]:
                    return self.board[x1][y1]
        if self.step == 9:
            return "draw"
        return False

    def ai_step(self):  # artificial intellect`s step
        x, y = self.get_key(random.randint(0, 8))
        if self.board[x][y] != "X" and self.board[x][y] != "O":
            self.board[x][y] = "O"
            self.step += 1
        else:
            self.ai_step()

    def get_key(self, value_need):
        for key, value in self.coord_ratio.items():
            if value == value_need:
                return key
