# Tilemap CSV Key/Legend

## Tile Values and Their Meanings

| Value | Description | Color | Collision |
|-------|-------------|-------|-----------|
| `-1`  | Empty space (transparent) | Sky blue background | No collision |
| `0`   | Empty space (transparent) | Sky blue background | No collision |
| `1`   | Ground tiles | Brown `(139, 69, 19)` | Solid collision |
| `2`   | Platform tiles | Grey `(100, 100, 100)` | Solid collision |
| `3`   | Platform tiles | Grey `(100, 100, 100)` | Solid collision |
| `4`   | **Visible hazards** | Red spikes `(220, 20, 20)` | **DEADLY** - Kills player |
| `5`   | **Invisible hazards** | Transparent | **DEADLY** - Kills player |

## Map Layout Information

- **Dimensions**: 18 rows × 80 columns
- **Tile Size**: 32×32 pixels
- **Total Map Width**: 2560 pixels (80 × 32)
- **Total Map Height**: 576 pixels (18 × 32)

## Usage Guidelines

### Ground Tiles (Type 1 - Brown)
- Use for the main ground/floor that the player runs on
- Typically placed in the bottom rows (15-17)
- Should form continuous surfaces for running

### Platform Tiles (Types 2 & 3 - Grey)
- Use for floating platforms that players can jump on
- Can be placed anywhere in the air
- Types 2 and 3 are functionally identical (both grey, both solid)
- Use different numbers to distinguish platform groups if needed

### Hazard Tiles (Types 4 & 5 - DEADLY)
- **Type 4 - Visible Hazards**: Red spikes that are clearly visible to players
  - Use on ground level as obstacles to jump over
  - Shows bright red color with spike pattern
  - Instantly kills player on contact
- **Type 5 - Invisible Hazards**: Transparent death zones
  - Use as pitfalls or hidden traps
  - Completely invisible to players
  - Instantly kills player on contact
  - Perfect for creating challenging platforming sections

### Empty Spaces (Types -1 & 0)
- Use `-1` for standard empty space
- Use `0` for empty space (functionally identical to -1)
- These areas show the sky blue background
- Player and other entities can move through these spaces

## Infinite Looping

The map repeats infinitely horizontally:
- When the player reaches column 79, the next column wraps to column 0
- This creates a seamless infinite runner experience
- The pattern repeats endlessly as the player runs forward

## Editing the Map

1. Open `src/scenes/scene_1/map.csv` in any text editor
2. Modify values according to the key above
3. Save the file
4. Run the game to see changes immediately
5. Use this key to ensure proper tile placement and colors

### Hazard Placement Tips
- **Visible hazards (4)**: Place on ground level as jump obstacles
- **Invisible hazards (5)**: Use as pitfalls between platforms or hidden traps
- Test hazard placement to ensure fair but challenging gameplay
- Combine visible and invisible hazards for varied difficulty

### Death and Respawn System
- Player dies instantly when touching any hazard (types 4 or 5)
- Death screen appears with transparent overlay
- Options: **Retry** (respawn at start) or **Quit** (exit game)
- Use W/S or ↑/↓ to navigate menu, ENTER/SPACE to select