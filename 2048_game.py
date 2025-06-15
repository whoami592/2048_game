import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4
TILE_SIZE = 100
GRID_MARGIN = 10
WINDOW_SIZE = GRID_SIZE * (TILE_SIZE + GRID_MARGIN) + GRID_MARGIN
FPS = 60

# Colors
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
TEXT_COLOR = (119, 110, 101)
BANNER_COLOR = (50, 50, 50)
BANNER_TEXT_COLOR = (255, 255, 255)

# Font setup
FONT = pygame.font.SysFont("Arial", 40, bold=True)
BANNER_FONT = pygame.font.SysFont("Arial", 20, bold=True)

# Game class
class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 50))
        pygame.display.set_caption("2048 Game")
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_new_tile()
        self.add_new_tile()
        self.game_over = False

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice([2, 4])

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        # Draw banner
        pygame.draw.rect(self.screen, BANNER_COLOR, (0, 0, WINDOW_SIZE, 50))
        banner_text = BANNER_FONT.render("2048 Game - Coded by Pakistani Ethical Hacker Mr Sabaz Ali Khan", True, BANNER_TEXT_COLOR)
        self.screen.blit(banner_text, (10, 15))
        # Draw grid
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                tile_color = TILE_COLORS.get(value, TILE_COLORS[2048])
                pygame.draw.rect(self.screen,
                               tile_color,
                               (j * (TILE_SIZE + GRID_MARGIN) + GRID_MARGIN,
                                i * (TILE_SIZE + GRID_MARGIN) + GRID_MARGIN + 50,
                                TILE_SIZE, TILE_SIZE),
                               border_radius=5)
                if value > 0:
                    text = FONT.render(str(value), True, TEXT_COLOR)
                    text_rect = text.get_rect(center=(j * (TILE_SIZE + GRID_MARGIN) + GRID_MARGIN + TILE_SIZE // 2,
                                                    i * (TILE_SIZE + GRID_MARGIN) + GRID_MARGIN + 50 + TILE_SIZE // 2))
                    self.screen.blit(text, text_rect)
        pygame.display.flip()

    def move_left(self):
        moved = False
        for i in range(GRID_SIZE):
            # Extract non-zero tiles
            tiles = [self.grid[i][j] for j in range(GRID_SIZE) if self.grid[i][j] != 0]
            # Merge tiles
            new_tiles = []
            j = 0
            while j < len(tiles):
                if j + 1 < len(tiles) and tiles[j] == tiles[j + 1]:
                    new_tiles.append(tiles[j] * 2)
                    j += 2
                else:
                    new_tiles.append(tiles[j])
                    j += 1
            # Pad with zeros
            new_tiles += [0] * (GRID_SIZE - len(new_tiles))
            # Check if moved
            if new_tiles != [self.grid[i][j] for j in range(GRID_SIZE)]:
                moved = True
            # Update grid
            for j in range(GRID_SIZE):
                self.grid[i][j] = new_tiles[j]
        return moved

    def move(self, direction):
        moved = False
        # Save original grid
        original_grid = [row[:] for row in self.grid]
        
        if direction == "left":
            moved = self.move_left()
        elif direction == "right":
            # Reverse rows, move left, reverse back
            for i in range(GRID_SIZE):
                self.grid[i] = self.grid[i][::-1]
            moved = self.move_left()
            for i in range(GRID_SIZE):
                self.grid[i] = self.grid[i][::-1]
        elif direction == "up":
            # Transpose, move left, transpose back
            self.grid = [list(row) for row in zip(*self.grid)]
            moved = self.move_left()
            self.grid = [list(row) for row in zip(*self.grid)]
        elif direction == "down":
            # Transpose, reverse rows, move left, reverse back, transpose back
            self.grid = [list(row) for row in zip(*self.grid)]
            for i in range(GRID_SIZE):
                self.grid[i] = self.grid[i][::-1]
            moved = self.move_left()
            for i in range(GRID_SIZE):
                self.grid[i] = self.grid[i][::-1]
            self.grid = [list(row) for row in zip(*self.grid)]
        
        # If moved, add new tile
        if moved:
            self.add_new_tile()
        
        # Check game over
        if not moved and not any(0 in row for row in self.grid):
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if (j < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]) or \
                       (i < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]):
                        return moved
            self.game_over = True
        return moved

async def main():
    game = Game2048()
    
    def setup():
        game.draw()
    
    async def update_loop():
        if not game.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.move("left")
                    elif event.key == pygame.K_RIGHT:
                        game.move("right")
                    elif event.key == pygame.K_UP:
                        game.move("up")
                    elif event.key == pygame.K_DOWN:
                        game.move("down")
            game.draw()
    
    setup()
    while not game.game_over:
        await update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())