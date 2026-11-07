import pygame
import random
import sys

# Initialisation
pygame.init()

# Dimensions
WIDTH = 800
HEIGHT = 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (83, 83, 83)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Police
font = pygame.font.SysFont("Arial", 24)

# Classe Dino
class Dino:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 70
        self.width = 40
        self.height = 40
        self.vel_y = 0
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

    def move(self):
        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.y >= HEIGHT - 70:
            self.y = HEIGHT - 70
            self.on_ground = True

    def draw(self):
        pygame.draw.rect(WIN, BLACK, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# Classe Obstacle
class Obstacle:
    def __init__(self):
        self.x = WIDTH
        self.y = HEIGHT - 60
        self.width = 20
        self.height = 50
        self.speed = 6

    def move(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(WIN, BLACK, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def main():
    dino = Dino()
    obstacles = []
    spawn_timer = 0
    score = 0
    game_over = False

    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)

        # Sol
        pygame.draw.rect(WIN, GROUND_COLOR, (0, HEIGHT - 30, WIDTH, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    dino.jump()
                if event.key == pygame.K_r and game_over:
                    main()

        if not game_over:
            dino.move()

            spawn_timer += 1
            if spawn_timer > 90:
                obstacles.append(Obstacle())
                spawn_timer = 0

            for obstacle in obstacles[:]:
                obstacle.move()
                if obstacle.x < -50:
                    obstacles.remove(obstacle)
                    score += 1

                if dino.get_rect().colliderect(obstacle.get_rect()):
                    game_over = True

        dino.draw()

        for obstacle in obstacles:
            obstacle.draw()

        # Score
        score_text = font.render(f"Score: {score}", True, BLACK)
        WIN.blit(score_text, (650, 20))

        if game_over:
            over_text = font.render("GAME OVER - Press R to Restart", True, BLACK)
            WIN.blit(over_text, (200, 180))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
