from settings import *

class Score:
    def __init__(self, high_score=0):
        # General
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.display_surface = pygame.display.get_surface()

        # Paths
        font_path = join(BASE_PATH, "gfx", "Russo_One.ttf")

        # Font
        self.font = pygame.font.Font(font_path, 30)

        # Increment
        self.increment_height = self.surface.get_height() / 3

        # Data
        self.score = 0
        self.level = 1
        self.lines = 0
        self.high_score = high_score

    def display_text(self, pos, text, color="white"):
        text_surface = self.font.render(f"{text[0]}: {text[1]}", True, color)
        text_rect = text_surface.get_rect(center = pos)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        self.surface.fill(GRAY)
        
        # Determine score color (Gold/Yellow if high score beaten or tied)
        score_color = "white"
        if self.score > 0 and self.score >= self.high_score:
            score_color = YELLOW

        for i, text in enumerate([("Score", self.score), ("Level", self.level), ("Lines", self.lines)]):
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height
            
            # Apply color only to the Score text
            color = score_color if text[0] == "Score" else "white"
            self.display_text((x, y), text, color)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
