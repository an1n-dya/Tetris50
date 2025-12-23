from settings import *

from timer import Timer

class Game:
    def __init__(self, get_next_shape, update_score):
        # General
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # Game Connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        # Lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # Tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data)

        # Timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            "vertical move": Timer(self.down_speed, True, self.move_down),
            "horizontal move": Timer(MOVE_WAIT_TIME),
            "rotate": Timer(ROTATE_WAIT_TIME),
            "hard_drop": Timer(DROP_WAIT_TIME)
        }
        self.timers["vertical move"].activate()

        # Score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

        # Game Over
        self.game_over = False
        
        # Input Lock (prevent immediate input on game start)
        self.input_locked = True
        self.input_lock_timer = Timer(INPUT_LOCK_TIME, False, self.unlock_input)
        self.input_lock_timer.activate()
        
        # Paths
        font_path = join(BASE_PATH, "gfx", "Russo_One.ttf")
        
        self.font = pygame.font.Font(font_path, 40)
    
    def unlock_input(self):
        self.input_locked = False

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        if self.current_lines >= self.current_level * 5:
            self.current_level += 1
            self.down_speed *= 0.9
            self.down_speed_faster = self.down_speed * 0.8
            self.timers["vertical move"].duration = self.down_speed

        self.update_score(self.current_lines, self.current_score, self.current_level)

    def create_new_tetromino(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                self.game_over = True
                for timer in self.timers.values():
                    timer.deactivate()
                return

        self.check_finished_rows()
        self.tetromino = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data)

        if self.check_game_over():
            self.game_over = True
            for timer in self.timers.values():
                timer.deactivate()

    def check_game_over(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                continue
            if self.field_data[int(block.pos.y)][int(block.pos.x)]:
                return True
        return False

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()
        
        # Update input lock timer
        if self.input_locked:
            self.input_lock_timer.update()

    def move_down(self):
        self.tetromino.move_down()
    
    def hard_drop(self):
        drop_distance = 0
        while not self.tetromino.next_move_vertical_collide(self.tetromino.blocks, drop_distance + 1):
            drop_distance += 1
        
        for block in self.tetromino.blocks:
            block.pos.y += drop_distance
        
        # Add bonus points for hard drop
        self.current_score += drop_distance * 2
        self.update_score(self.current_lines, self.current_score, self.current_level)
        
        # Lock the piece
        for block in self.tetromino.blocks:
            if block.pos.y >= 0:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
        self.create_new_tetromino()
    
    def get_shadow_positions(self):
        drop_distance = 0
        while not self.tetromino.next_move_vertical_collide(self.tetromino.blocks, drop_distance + 1):
            drop_distance += 1
        
        shadow_positions = []
        for block in self.tetromino.blocks:
            shadow_pos = pygame.Vector2(block.pos.x, block.pos.y + drop_distance)
            shadow_positions.append(shadow_pos)
        
        return shadow_positions
        
    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1)

        for row in range (1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y), 1)

        self.surface.blit(self.line_surface, (0, 0))

    def draw_shadow(self):
        shadow_positions = self.get_shadow_positions()
        shadow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        shadow_surface.fill(self.tetromino.color)
        shadow_surface.set_alpha(80)
        
        for pos in shadow_positions:
            if pos.y >= 0:
                rect = shadow_surface.get_rect(topleft=(pos.x * CELL_SIZE, pos.y * CELL_SIZE))
                self.surface.blit(shadow_surface, rect)

    def input(self):
        # Don"t accept input during grace period
        if self.input_locked:
            return
            
        keys = pygame.key.get_pressed()

        # Checking Horizontal Movement
        if not self.timers["horizontal move"].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers["horizontal move"].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers["horizontal move"].activate()

        # Check For Rotation
        if not self.timers["rotate"].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers["rotate"].activate()

        # Hard Drop with Space
        if not self.timers["hard_drop"].active:
            if keys[pygame.K_SPACE]:
                self.hard_drop()
                self.timers["hard_drop"].activate()

        # Down Speedup
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers["vertical move"].duration = self.down_speed_faster

        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers["vertical move"].duration = self.down_speed

    def check_finished_rows(self):
        # Get The Full Row Indexes
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                # Delete Full Rows
                for block in self.field_data[delete_row]:
                    block.kill()

                # Move Down Blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

            # Rebuild the Field Data
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                if block.pos.y >= 0:
                    self.field_data[int(block.pos.y)][int(block.pos.x)] = block
        
            # Update Score
            self.calculate_score(len(delete_rows))

    def run(self):
        # Update
        if not self.game_over:
            self.input()
            self.timer_update()
            self.sprites.update()

        self.draw()

        if self.game_over:
            self.draw_game_over()

    def draw(self):
        self.surface.fill(GRAY)
        
        # Draw shadow before actual pieces
        if not self.game_over:
            self.draw_shadow()
        
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

    def draw_game_over(self):
        text_surf = self.font.render("GAME OVER", True, "white")
        text_rect = text_surf.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2))
        
        bg_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(self.display_surface, "black", bg_rect.move(PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, bg_rect.move(PADDING, PADDING), 2)
        
        self.display_surface.blit(text_surf, text_rect.move(PADDING, PADDING))

class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):
        # Setup
        self.shape = shape
        self.block_positions = TETROMINOS[shape]["shape"]
        self.color = TETROMINOS[shape]["color"]
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        # Create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    # Collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collison_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
        return True if any(collison_list) else False

    def next_move_vertical_collide(self, blocks, amount):
        collison_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
        return True if any(collison_list) else False

    # Movement
    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                if block.pos.y >= 0:
                    self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    # Rotate
    def rotate(self):
        if self.shape != "O":
            # Pivot Point
            pivot_pos = self.blocks[0].pos

            # New Block Position
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # Collision Check
            for pos in new_block_positions:
                # Horizontal Check
                if pos.x < 0 or pos.x >= COLUMNS:
                    return

                # Vertical / Floor Check
                if pos.y >= ROWS:
                    return

                # Field Check ->  Collision With Other Pieces
                if pos.y >= 0 and self.field_data[int(pos.y)][int(pos.x)]:
                    return

            # Implement New Positions
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        # General
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # Position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)

    def rotate(self, pivot_pos):
        # Block Rotation Calculation
        return pivot_pos + (self.pos - pivot_pos).rotate(90)

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True

        if self.pos.y >= 0 and field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True

        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE
