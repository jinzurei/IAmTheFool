import pygame
from core import settings
from entities.player import Player
from entities.obstacle import Obstacle
from entities.background import Background
from entities.ground import Ground

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Endless Runner - Basic")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont(None, 36)

        self.player = Player()
        self.obstacle = Obstacle()
        self.background = Background()
        self.ground = Ground()

        self.hit = False

        self.current_region = 0
        self.distance_traveled = 0
        self.region_change_threshold = 2000

    def run(self):
        while self.running:
            keys = pygame.key.get_pressed()
            self.handle_events()
            self.update(keys)
            self.draw()
            self.clock.tick(settings.FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player.handle_event(event)

    def update(self, keys):
        self.player.update(keys)
        self.obstacle.update()
        self.background.update()
        self.ground.update()

        # Distance-based region switching
        self.distance_traveled += settings.SCROLL_SPEED
        if self.distance_traveled >= self.region_change_threshold:
            self.distance_traveled = 0
            self.current_region = (self.current_region + 1) % 3
            self.background.set_region(self.current_region)
            self.ground.current_color_index = self.current_region
            self.ground.color = self.ground.colors[self.current_region]

        # Collision detection
        if self.player.get_rect().colliderect(self.obstacle.get_rect()):
            self.hit = True
        else:
            self.hit = False

    def draw(self):
        self.background.draw(self.screen)
        self.ground.draw(self.screen)
        self.player.draw(self.screen)
        self.obstacle.draw(self.screen)

        if self.hit:
            text = self.font.render("Collision!", True, settings.BLACK)
            self.screen.blit(text, (settings.SCREEN_WIDTH // 2 - 60, 20))

        pygame.display.flip()