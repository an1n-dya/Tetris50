from settings import *
from sys import exit

from random import choice, shuffle

# Components
from game import Game
from score import Score
from preview import Preview
from start_menu import StartMenu

class Main:
    def __init__(self):
        # General
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris 50")

        # Game state
        self.game_state = "menu"  # "menu" or "playing"
        
        # Start Menu
        self.start_menu = StartMenu()

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
                    
                    # Handle menu state
                    if self.game_state == "menu":
                        # Any key starts the game
                        self.game_state = "playing"
                        # Activate timers to prevent immediate input
                        self.game.timers["hard_drop"].activate()
                        self.game.timers["horizontal move"].activate()
                        self.game.timers["rotate"].activate()
                    
                    # Restart game after game over (any key except ESC)
                    elif self.game.game_over:
                        self.game = Game(self.get_next_shape, self.update_score)
                        self.score = Score()
                        # Activate timers to prevent immediate input on restart
                        self.game.timers["hard_drop"].activate()
                        self.game.timers["horizontal move"].activate()
                        self.game.timers["rotate"].activate()

            # Display based on game state
            if self.game_state == "menu":
                self.start_menu.run()
            else:
                self.display_surface.fill(GRAY)
                
                # Components
                self.game.run()
                self.score.run()
                self.preview.run(self.next_shapes)

            # Updating
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    main = Main()
    main.run()
