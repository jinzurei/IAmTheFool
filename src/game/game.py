import pygame
from typing import Tuple, List
from src.config import settings
from src.core.camera import YSortCameraGroup
from src.entities.player import Player
from src.entities.tile import StaticTile

class Game:
    """Main game class that manages the game loop and entities."""
    def __init__(self) -> None:
        """Initialize the game with all necessary components."""
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("I Am The Fool")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont(None, 36)

        # Game state management
        self.game_state = settings.MENU

        # Camera system
        self.camera = YSortCameraGroup()

        # Game entities (initialized when starting game)
        self.player = Player()
        self.obstacles = []  # Multiple obstacles for better world generation
        self.background = None
        self.ground = None

        self.collision_state = "none"  # none, collision, game_over
        self.current_region = 0
        self.distance_traveled = 0

    def run(self) -> None:
        """Run the main game loop."""
        while self.running:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            self.handle_events(events, keys)
            self.update(keys)
            self.draw()
    def draw(self):
        self.screen.fill(settings.BLUE)
        # Use camera's custom_draw to render all sprites
        self.camera.custom_draw(self.player)

    def handle_events(self, events: List[pygame.event.Event], keys: pygame.key.ScancodeWrapper) -> None:
        """Handle pygame events based on current game state."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
