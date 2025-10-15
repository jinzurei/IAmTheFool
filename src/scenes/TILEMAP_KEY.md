# Tilemap CSV Key/Legend

## Tile Values and Their Meanings

| Value | Description | Visual | Color | Collision | Notes |
|-------|-------------|--------|-------|-----------|-------|
| `0`   | Empty space | Sky/Background | Sky blue | No collision | Used for open air, nothing rendered |
| `1`   | Ground tile | Solid block | Brown `(139, 69, 19)` | Solid | Player stands/walks on these |
| `2`   | Platform tile | Thin platform | Grey `(100, 100, 100)` | Solid | Used for jumping, not ground |
| `3`   | Visible hazard | Red spikes | Red `(220, 20, 20)` | Deadly | Kills player on contact, clearly visible |
| `4`   | Invisible hazard | None (transparent) | None | Deadly | Kills player, not visible, for traps |
| `5`   | Spawn tile | Yellow square | Yellow `(255, 255, 0)` | No collision | Player spawns here |

## Map Layout Information

- **Dimensions**: 18 rows × 80 columns
- **Tile Size**: 32×32 pixels
- **Total Map Width**: 2560 pixels (80 × 32)
- **Total Map Height**: 576 pixels (18 × 32)

## Usage Notes

- Only values listed above are valid in the map CSV files.
- Hazards (`3` and `4`) instantly kill the player.
- Platforms (`2`) are for jumping, not for walking on ground level.
- Empty tiles (`0`) are not rendered and have no collision.

## Usage Guidelines

### Ground Tiles (Type 1 - Brown)
- Use for the main ground/floor that the player runs on
- Typically placed in the bottom rows (15-17)
- Should form continuous surfaces for running

### Platform Tiles (Type 2 - Grey)
- Use for floating platforms that players can jump on
- Can be placed anywhere in the air
- Only one platform tile type is used (2)

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