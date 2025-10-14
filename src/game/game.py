import pygame
from src.config import settings
from src.core.camera import YSortCameraGroup, CameraLookAhead
from src.entities.player import Player
from src.entities.tile import StaticTile

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("I Am The Fool")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont(None, 36)
        self.game_state = settings.MENU
        self.camera = YSortCameraGroup()
        self.cam_lookahead = CameraLookAhead()
        self.player = Player()
        self.obstacles = []
        self.background = None
        self.ground = None
    self.collision_state = "none"
    self.current_region = 0
    self.distance_traveled = 0
    def run(self):
        dt = 0
        while self.running:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_F6]:
                w, h = self.player.rect.size
                self.player.rect.size = (w, h + 1)
                self.player._rescale_draw_image_to_collider(self.player._art_pad)
            if keys[pygame.K_F7]:
                w, h = self.player.rect.size
                self.player.rect.size = (w, max(1, h - 1))
                self.player._rescale_draw_image_to_collider(self.player._art_pad)
            self.handle_events(events, keys)
            self.player.update(dt, self.obstacles)
            self.cam_lookahead.update(self.player.rect.center, dt)
            self.draw()
            dt = self.clock.tick(60) / 1000.0
    def draw(self):
        self.screen.fill(settings.BLUE)
        cam_offset = (int(self.cam_lookahead.offset.x), int(self.cam_lookahead.offset.y))
        self.player.draw(self.screen, camera_offset=cam_offset)
        for obstacle in self.obstacles:
            if hasattr(obstacle, 'draw'):
                obstacle.draw(self.screen, camera_offset=cam_offset)
            else:
                self.screen.blit(obstacle.image, obstacle.rect.move(-cam_offset[0], -cam_offset[1]))
    def handle_events(self, events, keys):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
