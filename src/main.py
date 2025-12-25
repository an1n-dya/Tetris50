from settings import *
from sys import exit

from random import shuffle

# Components
from game import Game
from score import Score
from preview import Preview
from start_menu import StartMenu

class Main:
    def __init__(self):
        # General
        pygame.init()
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris 50")

        # Game state
        self.game_state = "menu"  # "menu" or "playing"
        
        # High Score
        self.high_score = self.load_high_score()
        
        # Start Menu
        self.start_menu = StartMenu(self.high_score)

        # Theme Music
        self.music_path = join(BASE_PATH, "sfx", "theme.mp3")
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.muted = False
        self.paused = False

        # Components
        self._reset_game()
        
    def _reset_game(self):
        self.bag = []
        self.next_shapes = [self.get_from_bag() for shape in range(3)]
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score(self.high_score)
        self.preview = Preview()


    def load_high_score(self):
        try:
            with open(join(BASE_PATH, "highscore.txt"), "r") as file:
                return int(file.read())
        except:
            return 0

    def save_high_score(self):
        with open(join(BASE_PATH, "highscore.txt"), "w") as file:
            file.write(str(self.high_score))

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level
        
        if score > self.high_score:
            self.high_score = score
            self.save_high_score()
            self.score.high_score = self.high_score
            self.start_menu.high_score = self.high_score

    def get_from_bag(self):
        if not self.bag:
            self.bag = list(TETROMINOS.keys())
            shuffle(self.bag)
        return self.bag.pop()

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(self.get_from_bag())

        return next_shape

    def draw_pause(self):
        # Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        self.display_surface.blit(overlay, (0, 0))
        
        # Font
        font_path = join(BASE_PATH, "gfx", "Russo_One.ttf")
        font_large = pygame.font.Font(font_path, 50)
        font_small = pygame.font.Font(font_path, 24)
        
        # Text
        title_surf = font_large.render("PAUSED", True, YELLOW)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 40))
        self.display_surface.blit(title_surf, title_rect)
        
        resume_surf = font_small.render("Press ESC to Resume", True, "white")
        resume_rect = resume_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20))
        self.display_surface.blit(resume_surf, resume_rect)
        
        quit_surf = font_small.render("Press Q to Main Menu", True, "white")
        quit_rect = quit_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 55))
        self.display_surface.blit(quit_surf, quit_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    # ESC to pause/resume or exit
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state == "playing":
                            self.paused = not self.paused
                        else:
                            pygame.quit()
                            exit()

                    # Q to quit to menu when paused
                    elif event.key == pygame.K_q and self.paused:
                        self.paused = False
                        self.game_state = "menu"
                    
                    # Muting/Unmuting Theme
                    elif event.key == pygame.K_m:
                        if self.muted:
                            pygame.mixer.music.set_volume(0.5)
                            self.muted = False
                        else:
                            pygame.mixer.music.set_volume(0)
                            self.muted = True

                    # Handle menu state - Any key starts a new game
                    elif self.game_state == "menu":
                        self._reset_game() # Always start a fresh game from menu
                        self.game_state = "playing"
                        # Activate timers to prevent immediate input
                        self.game.timers["hard_drop"].activate()
                        self.game.timers["horizontal move"].activate()
                        self.game.timers["rotate"].activate()
                    
                    # Restart game after game over (any key except ESC)
                    elif self.game.game_over and not self.paused:
                        self._reset_game() # Reset game components for a new game
                        # Activate timers to prevent immediate input on restart
                        self.game.timers["hard_drop"].activate()
                        self.game.timers["horizontal move"].activate()
                        self.game.timers["rotate"].activate()

            # Display based on game state
            if self.game_state == "menu":
                if not self.start_menu.run(): # If run() returns False, it means a key was pressed and the menu should exit
                    self.game_state = "playing" # Transition to playing state
                    self._reset_game() # Always start a fresh game from menu
                    # Activate timers to prevent immediate input
                    self.game.timers["hard_drop"].activate()
                    self.game.timers["horizontal move"].activate()
                    self.game.timers["rotate"].activate()
            else:
                self.display_surface.fill(GRAY)
                
                if self.paused:
                    self.game.draw()
                    self.score.run()
                    self.preview.run(self.next_shapes)
                    self.draw_pause()
                else:
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
