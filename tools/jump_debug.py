import sys
import pathlib
import pygame
import importlib

# Ensure repo root and src are on sys.path so we can import the package-style modules
repo_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))
sys.path.insert(1, str(repo_root / 'src'))

from src.settings import JUMP_KEYS
from src.entities.player import Player

pygame.init()
# Minimal display so key module is ready
screen = pygame.display.set_mode((100, 100))

player = Player((200, 300), [])
print('Initial vel_y:', player.vel_y, 'pos:', player.pos)

orig_get = pygame.key.get_pressed
class FakeKeys:
    def __init__(self, true_keys):
        self.true = set(true_keys)

    def __getitem__(self, idx):
        return 1 if idx in self.true else 0

    def __iter__(self):
        # Provide a minimal iterator (not full keyset); only used for any()
        # in the Player code where explicit indices are fetched, so iteration
        # isn't required. But implement to be safe.
        return iter(())

# Monkeypatch get_pressed to return our fake keys with jump pressed
pygame.key.get_pressed = lambda: FakeKeys(JUMP_KEYS)

# Run a few frames and print state
for i in range(1, 6):
    dt = 1.0 / 60.0
    player.update(dt, pygame.sprite.Group())
    print(f"Frame {i}: vel_y={player.vel_y:.2f}, pos={player.pos}, rect={player.rect}")