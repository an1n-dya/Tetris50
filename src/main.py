from settings import *
from sys import exit

from random import choice, shuffle

# Components
from game import Game
from score import Score
from preview import Preview

class Main:
    def __init__(self):
        # General
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris 50")

        # Shapes
        self.bag = []
        self.next_shapes = [self.get_from_bag() for shape in range(3)]

        # Components
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_from_bag(self):
        if not self.bag:
            self.bag = list(TETROMINOS.keys())
            shuffle(self.bag)
        return self.bag.pop()

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(self.get_from_bag())

        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    # ESC to exit game
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    
                    # Restart game after game over (any key)
                    if self.game.game_over:
                        self.game = Game(self.get_next_shape, self.update_score)
                        self.score = Score()

            # Display
            self.display_surface.fill(GRAY)

            # Components
            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)

            # Updating
            pygame.display.update()
            self.clock.tick()

if __name__ == "__main__":
    main = Main()
    main.run()
