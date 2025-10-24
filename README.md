# I Am the Fool 🎭

A personal experiment in code and control — built from the ground up in **Python** and **Pygame**.  
This project isn’t just a game; it’s a mirror of process, failure, and the art of precision.

> "This is me versus me — the architect and the fool, both fighting to evolve."

---

## 🎮 Overview

**I Am the Fool** is a modular 2D platformer engine built in Python/Pygame, focused on clean architecture and precise movement physics. It serves as a sandbox for refining motion feel, camera logic, and region-based world design.

### Core Features
- ⚙️ **Custom Engine:** Separated into `core/`, `entities/`, and `scenes/` for clean modularity and fast iteration.
- 🧠 **Physics System:** Delta-time–based gravity, coyote time, jump buffering, and variable-height jumps using easing functions.
- 🧍‍♂️ **Player Controller:** Supports walking, jumping, and dashing with smooth acceleration and grounded detection.
- 🧱 **Collision Detection:** Axis-based resolution with predictive correction using stored `prev_bottom` and `prev_rect` values.
- 🌀 **Camera & Parallax:** Camera smoothly follows the player; layered parallax backgrounds create depth.
- 🌍 **Region Logic:** CSV-defined maps with spawn points and transitions between scenes.

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

### ⚙️ Core Motion (Symplectic / Semi-Implicit Euler, Discrete Time)

The following describes the discrete-time motion model used throughout *I Am the Fool*.  
Most Pygame examples integrate motion per frame (`pos += vel; vel += g`), which ties physics directly to FPS and can cause drift or instability. This engine instead uses a **symplectic (semi-implicit) Euler** integrator, where velocity is updated first and the new velocity drives position.

The result is stable, frame-rate–independent physics with consistent acceleration, jump arcs, and easing across all frame rates. All forces; gravity, input acceleration, dash impulses, and easing—are expressed in consistent pixel-space units and integrated using Δt = 1/FPS.

Let Δt = 1/FPS (seconds). Positions and velocities are updated at discrete steps n → n+1.

#### Velocity update
vx_{n+1} = vx_n + a_x^{input}(n)·Δt + v_dash,0 · exp(−k_dash · τ_n)         # dash is a velocity term [px/s]
vy_{n+1} = vy_n + g · M(n) · Δt                                              # gravity acts only on y

#### Optional easing during ascent (vy_{n+1} < 0)
vy_{n+1} ← vy_{n+1} · clamp( 1 − k_ease · e(u_n)^{p} , 0 , 1 )

#### Terminal fall speed (positive-down convention)
vy_{n+1} ← min( vy_{n+1}, V_fall,max )

#### Position update (semi-implicit: uses updated velocity)
x_{n+1} = x_n + vx_{n+1} · Δt
y_{n+1} = y_n + vy_{n+1} · Δt

---

**Parameters and units**

- g = 1400 px/s² (downward).
- M(n) ∈ { 1.0, 1.7, 1.8 } is a piecewise multiplier on gravity (vertical only):
  - 1.0 while rising with normal hold,
  - 1.7 (LOW_JUMP_MULTIPLIER) on early release,
  - 1.8 (FALL_MULTIPLIER) when falling (vy_n ≥ 0).
- a_x^{input}(n) is horizontal acceleration [px/s²]. In code it’s typically
  a_x^{input}(n) = (v_target − vx_n) · ACCEL_RATE.
- v_dash,0 [px/s] is the initial dash velocity contribution; k_dash [1/s] is the decay rate; τ_n [s] is time since dash start.
- Easing: k_ease = 0.25, p = 1.2, e(·) ∈ {cubic, quint}; u_n ∈ [0,1] is normalized ascent progress.
  The factor `clamp(…)` is bounded in [0,1] to preserve dimensions and avoid overshoot.
- V_fall,max = MAX_FALL_SPEED = 2600 px/s.
- Δt ≈ 1/60 s (for FPS = 60).

**Notes**
- Scheme is **symplectic (semi-implicit) Euler**: first-order accurate in time, energy-dissipative and stable for platformer kinematics at small Δt.
- All quantities have consistent units (px, px/s, px/s²). Dash is explicitly a **velocity** term; if modeled as acceleration instead, replace `v_dash,0 · exp(−k_dash · τ_n)` with `[a_dash,0 · exp(−k_dash · τ_n)] · Δt` and set units to px/s².

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
