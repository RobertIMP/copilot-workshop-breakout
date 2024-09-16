import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 10
BALL_SIZE = 10
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 20
LIVES = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

# Font setup
font = pygame.font.SysFont(None, 36)

# Platform class
class Platform:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2, SCREEN_HEIGHT - 30), (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.speed = 10

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_SIZE, BALL_SIZE))
        self.dx = random.choice([-4, 4])
        self.dy = -4

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy

    def draw(self):
        pygame.draw.ellipse(screen, RED, self.rect)

# Block class with color and hit points
class Block:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.color = color
        self.hit_points = 3 if color == RED else 1

    def hit(self):
        self.hit_points -= 1
        if self.color == RED:
            fade_amount = 85  # 255 / 3 hits = 85
            new_red_value = max(0, self.color[0] - fade_amount)
            self.color = (new_red_value, 0, 0)
        return self.hit_points <= 0

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Create blocks with different colors
block_colors = [RED, GREEN, BLUE, WHITE]
blocks = []
for i in range(5):
    for j in range(10):
        if i == 4:
            color = YELLOW
        else:
            color = block_colors[i % len(block_colors)]
        blocks.append(Block(j * (BLOCK_WIDTH + 10) + 35, i * (BLOCK_HEIGHT + 10) + 50, color))

# Main game loop
def main():
    platform = Platform()
    balls = [Ball()]
    lives = LIVES
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            platform.move("left")
        if keys[pygame.K_d]:
            platform.move("right")

        for ball in balls[:]:
            ball.move()

            # Ball collision with platform
            if ball.rect.colliderect(platform.rect):
                ball.dy = -ball.dy

            # Ball collision with blocks
            for block in blocks[:]:
                if ball.rect.colliderect(block.rect):
                    ball.dy = -ball.dy
                    if block.hit():
                        blocks.remove(block)
                        if block.color == WHITE:
                            balls.append(Ball())

            # Ball falls below platform
            if ball.rect.bottom >= SCREEN_HEIGHT:
                balls.remove(ball)
                if not balls:
                    lives -= 1
                    if lives == 0:
                        print("Game Over")
                        pygame.quit()
                        sys.exit()
                    balls.append(Ball())

        # Win condition
        if not blocks:
            print("You Win!")
            pygame.quit()
            sys.exit()

        platform.draw()
        for ball in balls:
            ball.draw()
        for block in blocks:
            block.draw()

        # Display lives
        lives_text = font.render(f'Lives: {lives}', True, WHITE)
        screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()