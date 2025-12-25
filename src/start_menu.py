from settings import *

import math
from random import randint, choice

class StartMenu:
    def __init__(self, high_score=0):
        self.display_surface = pygame.display.get_surface()
        self.high_score = high_score
        
        # Paths
        font_path = join(BASE_PATH, "gfx", "Russo_One.ttf")
        logo_path = join(BASE_PATH, "gfx", "LOGO.png")
        
        # Load and scale logo
        self.original_logo = pygame.image.load(logo_path).convert_alpha()
        self.logo_aspect_ratio = self.original_logo.get_width() / self.original_logo.get_height()
        
        # Scale logo to fit within a portion of the screen width
        self.logo_max_width = WINDOW_WIDTH * 0.7  # 70% of window width
        self.logo_width = int(self.logo_max_width)
        self.logo_height = int(self.logo_width / self.logo_aspect_ratio)
        
        # If height is too large, scale by height instead
        logo_max_height = WINDOW_HEIGHT * 0.4  # 40% of window height
        if self.logo_height > logo_max_height:
            self.logo_height = int(logo_max_height)
            self.logo_width = int(self.logo_height * self.logo_aspect_ratio)
        
        self.logo = pygame.transform.smoothscale(self.original_logo, (self.logo_width, self.logo_height))
        self.logo_rect = self.logo.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.3))
        
        # Fonts
        self.instruction_font = pygame.font.Font(font_path, 24)
        
        # Animation variables
        self.time = 0
        self.pulse_speed = 0.05
        
        # Colors for background blocks
        self.colors = [CYAN, BLUE, PURPLE, RED, ORANGE, YELLOW, GREEN]
        
        # Falling blocks for background
        self.bg_blocks = []
        self.spawn_timer = 0
        self.spawn_delay = 30
        
        # Layout constants (proportional to window size)
        self.high_score_y_ratio = 0.55   # 55% down the screen
        self.instruction_y_ratio = 0.65  # 65% down the screen
        self.controls_y_ratio = 0.75     # 75% down the screen
        self.control_spacing = 25        # Pixels between control lines
        self.credits_y_ratio = 0.95      # 95% down the screen (bottom)
        
        # Initialize some background blocks
        for _ in range(15):
            self.spawn_background_block()

    def spawn_background_block(self):
        x = randint(0, WINDOW_WIDTH)
        y = randint(-WINDOW_HEIGHT, 0)
        color = choice(self.colors)
        speed = randint(1, 3)
        size = randint(20, 40)
        self.bg_blocks.append({
            "x": x,
            "y": y,
            "color": color,
            "speed": speed,
            "size": size,
            "rotation": randint(0, 360)
        })
    
    def update_background(self):
        # Spawn new blocks periodically
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_background_block()
            self.spawn_timer = 0
        
        # Update existing blocks
        for block in self.bg_blocks[:]:
            block["y"] += block["speed"]
            block["rotation"] = (block["rotation"] + 1) % 360
            
            # Remove blocks that are off screen
            if block["y"] > WINDOW_HEIGHT + block["size"]:
                self.bg_blocks.remove(block)
    
    def draw_background_blocks(self):
        for block in self.bg_blocks:
            # Create a surface for the block
            surf = pygame.Surface((block["size"], block["size"]), pygame.SRCALPHA)
            
            # Draw the block with transparency
            color_with_alpha = (*pygame.Color(block["color"])[:3], 30)
            pygame.draw.rect(surf, color_with_alpha, surf.get_rect(), border_radius=5)
            pygame.draw.rect(surf, (*pygame.Color(block["color"])[:3], 80), 
                           surf.get_rect(), 2, border_radius=5)
            
            # Rotate the surface
            rotated_surf = pygame.transform.rotate(surf, block["rotation"])
            rect = rotated_surf.get_rect(center=(block["x"], block["y"]))
            
            self.display_surface.blit(rotated_surf, rect)
    
    def draw_logo(self):
        # Subtle floating animation
        float_offset = math.sin(self.time * 0.03) * 10
        logo_pos = self.logo_rect.copy()
        logo_pos.y += float_offset
        
        # Draw shadow
        shadow_offset = 5
        shadow_surf = self.logo.copy()
        shadow_surf.fill((0, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
        shadow_rect = logo_pos.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        self.display_surface.blit(shadow_surf, shadow_rect)
        
        # Draw logo
        self.display_surface.blit(self.logo, logo_pos)

    def draw_high_score(self):
        if self.high_score > 0:
            text = f"High Score: {self.high_score}"
            score_surf = self.instruction_font.render(text, True, YELLOW)
            
            # Add a slight shadow/outline
            outline_surf = self.instruction_font.render(text, True, "black")
            
            center_pos = (WINDOW_WIDTH // 2, int(WINDOW_HEIGHT * self.high_score_y_ratio))
            rect = score_surf.get_rect(center=center_pos)
            
            # Draw outline (offset)
            outline_rect = rect.copy()
            outline_rect.x += 2
            outline_rect.y += 2
            self.display_surface.blit(outline_surf, outline_rect)
            
            self.display_surface.blit(score_surf, rect)
    
    def draw_instructions(self):
        # Pulsing "Press Any Key" text
        pulse = abs(math.sin(self.time * 0.08))
        alpha = int(150 + pulse * 105)
        
        instruction_text = "Press Any Key To Start"
        instruction_surf = self.instruction_font.render(instruction_text, True, "white")
        instruction_surf.set_alpha(alpha)
        instruction_rect = instruction_surf.get_rect(center=(WINDOW_WIDTH // 2, int(WINDOW_HEIGHT * self.instruction_y_ratio)))
        self.display_surface.blit(instruction_surf, instruction_rect)
        
        # Controls info with fade-in effect
        controls_y = int(WINDOW_HEIGHT * self.controls_y_ratio)
        controls_alpha = min(255, int(self.time * 2))
        
        controls = [
            "LEFT & RIGHT : Move",
            "UP : Rotate",
            "DOWN : Soft Drop",
            "SPACE : Hard Drop",
            "M : Mute/Unmute Theme",
            "ESC : Pause / Exit"
        ]
        
        small_font = pygame.font.Font(None, 20)
        for i, text in enumerate(controls):
            control_surf = small_font.render(text, True, (200, 200, 200))
            control_surf.set_alpha(controls_alpha)
            control_rect = control_surf.get_rect(center=(WINDOW_WIDTH // 2, controls_y + i * self.control_spacing))
            self.display_surface.blit(control_surf, control_rect)
    
    def draw_credits(self):
        # Credits at the bottom
        credits_y = int(WINDOW_HEIGHT * self.credits_y_ratio)
        credits_alpha = min(255, int(self.time * 2))
        
        small_font = pygame.font.Font(None, 18)
        
        # Creator name
        credit_text = "By: Anindya Adi Chowdhury"
        credit_surf = small_font.render(credit_text, True, (180, 180, 180))
        credit_surf.set_alpha(credits_alpha)
        credit_rect = credit_surf.get_rect(center=(WINDOW_WIDTH // 2, credits_y))
        self.display_surface.blit(credit_surf, credit_rect)
        
        # CS50x Final Project
        project_text = "CS50x Final Project"
        project_surf = small_font.render(project_text, True, (150, 150, 150))
        project_surf.set_alpha(credits_alpha)
        project_rect = project_surf.get_rect(center=(WINDOW_WIDTH // 2, credits_y - 18))
        self.display_surface.blit(project_surf, project_rect)
    
    def draw_decorative_border(self):
        # Animated border
        pulse = abs(math.sin(self.time * 0.05))
        border_color = (
            int(100 + pulse * 155),
            int(100 + pulse * 155),
            int(200 + pulse * 55)
        )
        
        # Draw multiple border lines for depth
        border_thickness = 2
        border_radius = 5
        for i in range(3):
            pygame.draw.rect(self.display_surface, border_color, 
                           (PADDING - i, PADDING - i, 
                            WINDOW_WIDTH - PADDING * 2 + i * 2, 
                            WINDOW_HEIGHT - PADDING * 2 + i * 2), 
                           border_thickness, border_radius)
    
    def run(self):
        # Update animations
        self.time += 1
        self.update_background()
        
        # Draw everything
        self.display_surface.fill(GRAY)
        self.draw_background_blocks()
        self.draw_decorative_border()
        self.draw_logo()
        self.draw_high_score()
        self.draw_instructions()
        self.draw_credits()
        
        return True  # Menu is still active

