# I Am the Fool 🎭

A solo game jam project exploring modular game design with **Python** and **Pygame**.
Built from scratch as a personal milestone after two semesters back in school.

> "This is me vs. me — and this time, I came to win."

---

## 🎮 Overview

**I Am the Fool** is a parallax-scrolling endless runner built entirely with rectangles and modular architecture. This prototype is a sandbox to test game development logic, clean structure, and region-based dynamic systems.

- 🌀 Parallax background and scrolling ground
- 🧍‍♂️ Player controls with WASD and dash physics
- 💥 Collision detection
- 🗺️ Region transitions

All logic is built in modules:
```bash
IAmTheFool/                         # Project root
├── .github/                        # GitHub-specific config (CI/CD, templates)
│   └── workflows/                  # Automation workflows for GitHub Actions
│       └── flake8.yml              # Lint job to run flake8 on pushes/PRs
│
├── .pytest_cache/                  # Auto-generated pytest cache (safe to ignore/clean)
│
├── assets/                         # Game art, audio, and other media
│   └── mage.samurai                # Example asset file (placeholder/demo)
│
├── entities/                       # Legacy/standalone entity modules outside src (keep or archive)
│   ├── background.py               # Old background entity implementation
│   ├── ground.py                   # Old ground platform entity
│   ├── obstacle.py                 # Old obstacle entity
│   ├── player.py                   # Old player entity (legacy copy)
│   └── scrollable.py               # Old scrolling helper/entity
│
├── scripts/                        # Utility scripts for local dev/automation
│   └── run_flake8.ps1              # Windows PowerShell helper to run flake8
│
├── src/                            # Main application source (authoritative code)
│   ├── core/                       # Engine primitives, math, and helpers
│   │   ├── camera.py               # Camera system + view transforms
│   │   ├── collision.py            # Collision detection/response routines
│   │   ├── constants.py            # Shared constants/enums/tunables
│   │   ├── sprite_align.py         # Utilities to align sprites to hitboxes/tiles
│   │   └── support.py              # Misc helpers (loading, timing, etc.)
│   │
│   ├── entities/                   # Runtime entity/component implementations
│   │   ├── enemies/                # Enemy subclasses (package directory)
│   │   ├── hazard.py               # Damage zones / traps
│   │   ├── player.py               # Active player entity (authoritative)
│   │   ├── tile.py                 # Tile objects + tile utilities
│   │   └── trigger.py              # Triggers/volumes for scripted events
│   │
│   ├── game/                       # Game orchestration and main loop glue
│   │   ├── engine.py               # Engine bootstrap, loop, systems wiring
│   │   └── game.py                 # Game state manager / scene coordination
│   │
│   ├── scenes/                     # Level data and scene-specific assets/scripts
│   │   ├── scene_1/                # Scene 1 data
│   │   │   └── testmap.csv         # CSV tilemap for scene 1
│   │   ├── scene_2/                # Scene 2 data
│   │   │   └── map.csv             # CSV tilemap for scene 2
│   │   ├── scene_3/                # Scene 3 data
│   │   │   └── map.csv             # CSV tilemap for scene 3
│   │   └── TILEMAP_KEY.md          # Documentation for tile IDs / semantics
│   │
│   ├── ui/                         # Screens and overlays
│   │   └── death_screen.py         # Game-over/death UI screen
│   │
│   ├── game.py                     # Top-level controller inside src (entry to gameplay code)
│   └── settings.py                 # The ONE authoritative settings config (display/FPS/physics)
│
├── tests/                          # Test suite and test config
│   ├── .flake8                     # Linting rules used during tests
│   ├── test_import_every_py.py     # Ensures modules import without errors
│   └── test_smoke_imports.py       # Basic smoke tests for package integrity
│
├── tools/                          # Dev utilities and one-off tools
│   └── jump_debug.py               # Visual/CLI jump-curve debugger
│
├── main.py                         # Repo-root launcher (calls into src/game.py)
├── CONTRIBUTING.md                 # How to contribute / dev workflow
├── CREDITS.md                      # Attributions/thanks
├── LICENSE                         # Project license
├── README.md                       # Documentation landing page (this file)
└── .gitignore                      # Files/folders to exclude from git
```

---

## 🧑‍💻 Who's This For?

This repo is **semi-public** and open for:
- 👀 Code review & feedback
- 🤝 Mentorship and exploration of my work
- 📬 Collaboration discussions

Please see [`CONTRIBUTING.md`](./CONTRIBUTING.md) before engaging.

---

## 🔧 Tech Stack

- Python 3.11+
- Pygame

---

## � Development notes

The repository-level flake8 configuration has been placed in `tests/.flake8` for local tooling
consistency with the project's test setup. If you run linters locally, please ensure your
editor or CI picks up `tests/.flake8` (or move it back to the repo root if you prefer a global
config file).

To run the project's flake8 consistently from the repo root, use the provided PowerShell
wrapper script:

	./scripts/run_flake8.ps1

This script invokes flake8 with the `tests/.flake8` config so contributors running the
script and CI run the same checks.


## �🚧 Roadmap Ideas (not guaranteed)

- Sprite animations for player
- Thematic backgrounds per region
- Ground textures with transitions
- Score counter, start menu, reset option

---

## 📜 License

MIT — Open for viewing, feedback, and discussion. Not a collaborative development project.

---

## ✨ Author

**Jin / jinzurei**  
🔗 [github.com/jinzurei](https://github.com/jinzurei)  
🐦 [@jinzurei](https://twitter.com/jinzurei)
