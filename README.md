# Tetris50
#### Video Demo: https://youtu.be/q2RXARs3DB4
#### Description:

Tetris50 is a complete implementation of classic Tetris built with Python and Pygame. The project features all standard Tetris mechanics plus modern enhancements like shadow piece preview, hard drop, wall kicks, persistent high scores, background music, sound effects, and pause functionality.

## What This Project Does

The game provides a 24×12 playing field where players manipulate falling tetromino pieces to clear lines and score points. As players progress, the game speeds up, creating increasing difficulty. The implementation includes proper piece rotation with wall kicks, collision detection, progressive leveling, and a preview system showing the next three pieces. High scores persist between sessions and are displayed prominently on the menu screen. The interface displays current score (highlighted in yellow when beating the high score), level, and lines cleared in a sidebar panel.

## File Structure

### Core Game Files

**main.py** - Entry point that initializes Pygame and its audio mixer, runs the main loop, and manages game state transitions between menu, playing, and paused states. Implements bag randomization where all seven pieces are shuffled together to ensure fair distribution. Handles high score loading from and saving to a file, background music playback with mute toggle, and pause overlay rendering. The _reset_game method cleanly resets all game components when starting fresh or returning from menu.

**game.py** - Contains three classes handling core gameplay. Game class manages the 24×12 grid, piece movement, collision detection, line clearing, and scoring. Now includes audio integration for game over and level up sounds, and enhanced hard drop scoring (0.4 points per cell for balance). Tetromino class handles piece rotation using vector mathematics with wall kick system that attempts rotation in default position, then tries kicking right, left, and up to allow rotation near walls and floor. Block class represents individual cells and manages positioning. Includes shadow piece calculation that simulates piece falling to show landing position.

**settings.py** - Centralizes all configuration: grid dimensions (24×12), cell size (40px), timing constants, color definitions for each piece type, tetromino shape coordinates, and scoring values (1/2/3/4 lines = 40/100/300/1200 points × level). Makes the game easily tunable and serves as the single source of truth for all constants.

**timer.py** - Reusable timer utility for time-based events. Manages vertical movement (piece drop speed), horizontal movement delays, rotation delays, hard drop cooldown, and input lock period. Timers can be single-shot or repeating with optional callbacks, keeping timing logic clean and consistent across the codebase.

### Interface Files

**score.py** - Displays score, level, and lines cleared in the right sidebar. Now accepts and displays high score, with visual feedback (yellow highlight) when current score meets or exceeds high score. Updates when lines are cleared and levels advance (every 5 lines). Handles text rendering and layout within the sidebar panel.

**preview.py** - Shows next three pieces using pre-rendered PNG images. Displays pieces vertically in the top portion of the right sidebar, allowing players to plan strategy multiple moves ahead.

**start_menu.py** - Animated start screen with game logo, falling background blocks with rotation effects, pulsing "Press Any Key" text, high score display (when available) in prominent yellow text with shadow effect, updated control instructions including new mute and pause controls, and credits. Uses sine wave calculations for smooth animations and demonstrates polish beyond minimum requirements.

### Supporting Files

**requirements.txt** - Lists pygame as the sole dependency for easy installation via pip.

**.gitignore** - Standard Python exclusions for bytecode, virtual environments, cache files, plus highscore.txt to prevent committing personal scores.

### Asset Files

**gfx/** contains the freely licensed Russo_One.ttf font, a custom LOGO.png, and individual PNG images for each tetromino shape (T.png, O.png, J.png, L.png, I.png, S.png, Z.png) used in the preview panel.

**sfx/** contains the audio assets, including theme.mp3 for continuously looping background music, game-over.mp3 that plays when the game ends, and next-level.mp3 that plays when the player advances to a new level.

## Design Decisions Explained

**Why Python/Pygame?** They provide an ideal balance of simplicity and control for learning game development without the complexity of full game engines while offering built-in audio support.

**Grid Size (24×12 vs standard 20×10)** - Extra vertical space makes the game more forgiving for beginners while maintaining core challenge and providing breathing room at spawn.

**Bag Randomization** - Instead of pure random selection, all seven pieces shuffle into a "bag" and each appears once before reshuffling. Prevents frustrating piece droughts while keeping gameplay unpredictable, matching modern Tetris standards.

**Wall Kicks** - When rotation would collide with walls or floor, the game attempts to "kick" the piece horizontally or vertically to complete the rotation. Tries default position first, then right (+1), left (-1), and up (-1). Makes rotation feel smooth and forgiving, especially for I-pieces near walls.

**Shadow Piece** - Shows where the current piece will land using semi-transparent rendering. Not in original Tetris but standard in modern versions because it improves playability and allows precise positioning without guesswork.

**Hard Drop (Space Bar)** - Instantly drops pieces to bottom and awards modest bonus points (0.4 per cell for balance). Enables faster gameplay for skilled players without making it the only viable strategy.

**High Score Persistence** - Saves high score to highscore.txt file between sessions. Displays on menu screen in yellow with shadow effect and highlights current score in yellow when matching or beating the record, providing clear visual feedback for achievement.

**Audio System** - Background music loops continuously at 50% volume to avoid fatigue. Sound effects trigger on level advancement and game over. Mute toggle (M key) allows players to silence audio without exiting. Enhances immersion and provides audio feedback for game events.

**Pause Functionality** - ESC pauses during gameplay, displaying dark overlay with resume and quit-to-menu options. Prevents accidental progress loss and allows players to take breaks. Game state freezes during pause, resuming exactly where it left off.

**Input Lock (300ms)** - Prevents the keypress that starts the game from immediately affecting gameplay. Small detail that significantly improves user experience by avoiding frustrating accidental moves.

**Progressive Difficulty** - Speed increases 10% every level (every 5 lines). It gradually raises the difficulty without sudden jumps, so the game stays challenging while still feeling fair as the player’s skills grow.

**Object-Oriented Design** - The game is built with a clear object oriented design where each part, such as the Game, Tetromino, Block, Score, Preview, and Menu, handles one specific responsibility. This separation keeps the codebase clean, easier to reason about, and much simpler to maintain or expand when adding new features later.

## Technical Highlights

The rotation algorithm uses pivot point calculations with vector mathematics to rotate pieces around their center block, enhanced with a four-stage wall kick system. Collision detection checks three conditions: wall boundaries, floor boundary, and existing blocks in the field grid. The timing system uses multiple independent timers to control different game aspects without interfering. File I/O safely handles high score persistence with exception handling for missing files. The audio mixer manages background music separately from sound effects, allowing independent control.

## How to Run

```bash
pip install -r requirements.txt
python src/main.py
```

**Controls:**
- Arrow Keys: Move left/right, rotate (up), soft drop (down)
- Space: Hard drop
- M: Mute/unmute audio
- ESC: Pause game / Resume / Exit
- Q: Quit to menu (when paused)

## What I Learned

Building Tetris50 taught me game loop architecture, state management, collision detection algorithms, and audio integration in games. Implementing piece rotation with wall kicks required understanding vector mathematics and iterative collision testing. Managing multiple timers for different game aspects showed me how to handle concurrent time-based events. Creating persistent high scores taught me file I/O and error handling. The pause system demonstrated proper game state management with overlay rendering.

The audio system integration showed me how to manage background music separately from sound effects, handle volume control, and trigger sounds based on game events. Implementing the wall kick system required careful testing of edge cases where pieces rotate near boundaries. Debugging the high score visual feedback taught me about conditional rendering and UI polish.

This project represents my growth through CS50x - from basic programming concepts to building a complete, feature-rich application with professional polish that I'm proud to share.
