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
IAmTheFool/
├── assets/                           # art, sound, and other media assets
│
├── src/
│   ├── config/                       # game-wide configuration values
│   │   └── settings.py               # display, FPS, and runtime setup
│   │
│   ├── core/                         # low-level engine logic and constants
│   │   ├── camera.py
│   │   ├── collision.py
│   │   ├── constants.py
│   │   ├── settings.py               # physics + movement constants
│   │   ├── sprite_align.py
│   │   └── support.py
│   │
│   ├── entities/                     # game entities and components
│   │   ├── enemies/
│   │   │   ├── __init__.py
│   │   │   ├── enemy.py
│   │   │   ├── mask.py
│   │   │   └── sprite.py
│   │   ├── hazard.py
│   │   ├── player.py
│   │   ├── tile.py
│   │   └── trigger.py
│   │
│   ├── game/                         # main game orchestration
│   │   ├── engine.py
│   │   ├── game.py
│   │   └── main.py
│   │
│   ├── scenes/                       # map CSVs and level scripts
│   │   ├── scene_1/
│   │   │   └── testmap.csv
│   │   ├── scene_2/
│   │   │   └── testmap.csv
│   │   ├── scene_3/
│   │   │   └── testmap.csv
│   │   └── TILEMAP_KEY.md
│   │
│   ├── systems/                      # engine subsystems (camera, physics, etc.)
│   │   └── camera.py
│   │
│   └── ui/                           # user interface and screens
│       └── death_screen.py
│
├── main.py                           # top-level launcher
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── CREDITS.md
└── .gitignore
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

## 🚧 Roadmap Ideas (not guaranteed)

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
