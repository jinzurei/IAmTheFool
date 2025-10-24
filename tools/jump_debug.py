import sys
import pathlib
import pygame


def main():
    # Ensure repo root and src are on sys.path so we can import package-style
    # modules from the local workspace.
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    sys.path.insert(1, str(repo_root / "src"))

    # Local imports after sys.path mutation to avoid E402 lint errors.
    from src import settings
    from src.entities.player import Player

    pygame.init()
    # Minimal display so key module is ready
    pygame.display.set_mode((100, 100))

    player = Player((200, 300), [])
    print("Initial vel_y:", player.vel_y, "pos:", player.pos)

    class FakeKeys:
        def __init__(self, true_keys):
            self.true = set(true_keys)

        def __getitem__(self, idx):
            return 1 if idx in self.true else 0

        def __iter__(self):
            # Provide a minimal iterator (not full keyset); only used for any()
            # in the Player code where explicit indices are fetched, so
            # iteration isn't required. But implement to be safe.
            return iter(())

    # Monkeypatch get_pressed to return our fake keys with jump pressed
    pygame.key.get_pressed = lambda: FakeKeys(settings.JUMP_KEYS)

    # Run a few frames and print state
    for i in range(1, 6):
        dt = 1.0 / 60.0
        player.update(dt, pygame.sprite.Group())
        print(f"Frame {i}: vel_y={player.vel_y:.2f}, pos={player.pos}, rect={player.rect}")


if __name__ == "__main__":
    main()
