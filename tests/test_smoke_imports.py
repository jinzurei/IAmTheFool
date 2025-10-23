import importlib


def test_core_modules_import():
    """Smoke test: import a small set of core modules to catch import errors.

    If any import raises, pytest will fail this test and surface the error in CI.
    """
    # Import only top-level importable modules. Note: there's a `src/game.py`
    # module and a `src/game/` package which may conflict; avoid importing
    # submodules under `src.game` to prevent package/module shadowing issues.
    modules = [
        "src.game",
        "src.entities.player",
        "src.core.camera",
        "src.ui.death_screen",
    ]
    for m in modules:
        importlib.import_module(m)
