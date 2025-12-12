import pygame
import random
from PIL import Image

# --- Configuration ---
WIDTH, HEIGHT = 1200, 720
FPS = 30
GIF_DURATION_SECONDS = 3  # How long the GIF should be
GIF_FILENAME = "matrix_rain_perspective.gif"

# Colors
BLACK = (0, 0, 0)
GREEN_BRIGHT = (0, 255, 70)
GREEN_DIM = (0, 100, 0)

# Character Set (Katakana + Numbers for that authentic look)
# If these don't render on your system, they will default to rectangles. 
# You can replace this string with "01" or "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHARS = "abcdefghijklmnopqrstuvwxyz1234567890" 

# --- Classes ---

class MatrixLayer:
    def __init__(self, font_size, speed, color, depth_alpha):
        self.font_size = font_size
        self.speed = speed
        self.color = color
        self.font = pygame.font.SysFont('arial', font_size, bold=True)
        self.columns = WIDTH // font_size
        # Each column has a random y position to start
        self.drops = [random.randint(-HEIGHT, 0) for _ in range(self.columns)]
        self.depth_alpha = depth_alpha # Transparency for depth effect

    def update_and_draw(self, surface):
        for i in range(len(self.drops)):
            # Draw the character
            char = random.choice(CHARS)
            char_render = self.font.render(char, True, self.color)
            
            # Apply alpha/transparency for depth perception (fading distant layers)
            char_render.set_alpha(self.depth_alpha)
            
            x_pos = i * self.font_size
            y_pos = self.drops[i]
            
            surface.blit(char_render, (x_pos, y_pos))
            
            # Move the drop down
            if y_pos > HEIGHT and random.random() > 0.95:
                self.drops[i] = random.randint(-50, 0) # Reset to top
            else:
                self.drops[i] += self.speed

def create_matrix_gif():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Matrix Digital Rain Generator")
    clock = pygame.time.Clock()

    # --- Create Layers for Perspective (Parallax) ---
    # Layer 1: Background (Small, Slow, Dim, Translucent)
    layer_bg = MatrixLayer(font_size=12, speed=3, color=GREEN_DIM, depth_alpha=100)
    
    # Layer 2: Midground (Medium size, Medium speed)
    layer_mg = MatrixLayer(font_size=20, speed=6, color=(0, 180, 50), depth_alpha=180)
    
    # Layer 3: Foreground (Large, Fast, Bright, Opaque)
    layer_fg = MatrixLayer(font_size=32, speed=10, color=GREEN_BRIGHT, depth_alpha=255)

    layers = [layer_bg, layer_mg, layer_fg]

    # Surface for the "trail" effect (fading)
    # We draw a semi-transparent black surface over everything to make old frames fade
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.set_alpha(30) # Lower number = longer trails
    fade_surface.fill(BLACK)

    frames = []
    total_frames = FPS * GIF_DURATION_SECONDS
    print(f"Generating {total_frames} frames. Please wait...")

    running = True
    frame_count = 0

    while running and frame_count < total_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Apply the fade effect (draw translucent black over previous frame)
        screen.blit(fade_surface, (0, 0))

        # 2. Update and draw all layers
        for layer in layers:
            layer.update_and_draw(screen)

        # 3. Update display
        pygame.display.flip()

        # 4. Capture the frame for GIF
        # Convert Pygame surface to string, then to PIL Image
        raw_str = pygame.image.tostring(screen, "RGB", False)
        image = Image.frombytes("RGB", (WIDTH, HEIGHT), raw_str)
        frames.append(image)

        frame_count += 1
        clock.tick(FPS)

    pygame.quit()

    # --- Save GIF ---
    print("Saving GIF... This might take a moment.")
    if frames:
        frames[0].save(
            GIF_FILENAME,
            save_all=True,
            append_images=frames[1:],
            optimize=False, # Set to True for smaller file size, False for better quality
            duration=1000 // FPS,
            loop=0
        )
        print(f"Done! Saved as {GIF_FILENAME}")

if __name__ == "__main__":
    create_matrix_gif()