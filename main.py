from src.game import Game
from src import settings

if __name__ == "__main__":
    # Print all top-level, uppercase entries from src/settings.py so we can
    # confirm exactly what configuration the process loaded at startup.
    try:
        setting_names = [n for n in dir(settings) if n.isupper()]
        print(f"[SETTINGS] {len(setting_names)} entries loaded from src/settings.py")
        for name in sorted(setting_names):
            try:
                val = getattr(settings, name)
                # Avoid printing very large structures in full; use repr
                print(f"{name} = {repr(val)}")
            except Exception as e:
                print(f"{name} = <error reading: {e}>")
    except Exception:
        # Never fail startup due to diagnostics
        pass
    game = Game()
    game.run()
