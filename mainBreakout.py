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

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

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

# Block class
class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# Create blocks
blocks = []
for i in range(5):
    for j in range(10):
        blocks.append(Block(j * (BLOCK_WIDTH + 10) + 35, i * (BLOCK_HEIGHT + 10) + 50))

# Main game loop
def main():
    platform = Platform()
    ball = Ball()
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

        ball.move()

        # Ball collision with platform
        if ball.rect.colliderect(platform.rect):
            ball.dy = -ball.dy

        # Ball collision with blocks
        for block in blocks[:]:
            if ball.rect.colliderect(block.rect):
                ball.dy = -ball.dy
                blocks.remove(block)

        # Ball falls below platform
        if ball.rect.bottom >= SCREEN_HEIGHT:
            lives -= 1
            ball = Ball()
            if lives == 0:
                print("Game Over")
                pygame.quit()
                sys.exit()

        # Win condition
        if not blocks:
            print("You Win!")
            pygame.quit()
            sys.exit()

        platform.draw()
        ball.draw()
        for block in blocks:
            block.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()