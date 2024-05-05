import pygame
import random

# Configurações do jogo
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Cores das peças
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0)]

# Formas das peças
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3],
     [3, 3]],

    [[4, 4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 0],
     [6, 0],
     [6, 6]],

    [[7, 0],
     [7, 0],
     [7, 0],
     [7, 0]]
]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.new_piece()
        self.score = 0
        self.font = pygame.font.SysFont(None, 30)

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        piece = {"shape": shape, "color": color, "x": BOARD_WIDTH // 2 - len(shape[0]) // 2, "y": 0}
        return piece

    def draw_board(self):
        self.screen.fill(BLACK)
        for y, row in enumerate(self.board):
            for x, block in enumerate(row):
                if block != 0:
                    pygame.draw.rect(self.screen, COLORS[block-1], (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for y, row in enumerate(self.current_piece["shape"]):
            for x, block in enumerate(row):
                if block != 0:
                    pygame.draw.rect(self.screen, self.current_piece["color"], ((self.current_piece["x"]+x)*BLOCK_SIZE, (self.current_piece["y"]+y)*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def check_collision(self, dx=0, dy=0):
        for y, row in enumerate(self.current_piece["shape"]):
            for x, block in enumerate(row):
                if block != 0:
                    if not 0 <= self.current_piece["x"]+x+dx < BOARD_WIDTH or not 0 <= self.current_piece["y"]+y+dy < BOARD_HEIGHT or self.board[self.current_piece["y"]+y+dy][self.current_piece["x"]+x+dx] != 0:
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece["shape"]):
            for x, block in enumerate(row):
                if block != 0:
                    self.board[self.current_piece["y"]+y][self.current_piece["x"]+x] = block
        self.current_piece = self.new_piece()
        if self.check_collision():
            return False
        return True

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.board) if all(row)]
        for line in lines_to_clear:
            del self.board[line]
            self.board.insert(0, [0] * BOARD_WIDTH)
            self.score += 100

    def draw_score(self):
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(score_text, (20, 20))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not self.check_collision(dx=-1):
                        self.current_piece["x"] -= 1
                    elif event.key == pygame.K_RIGHT and not self.check_collision(dx=1):
                        self.current_piece["x"] += 1
                    elif event.key == pygame.K_DOWN and not self.check_collision(dy=1):
                        self.current_piece["y"] += 1
                    elif event.key == pygame.K_SPACE:
                        while not self.check_collision(dy=1):
                            self.current_piece["y"] += 1

            if self.check_collision(dy=1):
                if not self.merge_piece():
                    running = False
                self.clear_lines()

            self.draw_board()
            self.draw_score()
            pygame.display.update()
            self.clock.tick(10)

        pygame.quit()

if __name__ == "__main__":
    Tetris().run()
