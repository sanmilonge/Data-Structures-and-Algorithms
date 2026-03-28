# ● Checkers

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)
![Interface](https://img.shields.io/badge/Interface-Terminal%20%2F%20Curses-black?style=for-the-badge&logo=gnometerminal&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)
![DSA](https://img.shields.io/badge/DSA-Minimax%20%7C%20Alpha--Beta%20%7C%20Backtracking-orange?style=for-the-badge)

> A fully-featured command-line Checkers game built in Python with a minimax AI, multi-jump chain captures, undo/redo history, variable board sizes, and two interface modes.

---

## ○ Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [How to Run](#-how-to-run)
- [How to Play](#-how-to-play)
- [Game Modes](#-game-modes)
- [Controls](#-controls)
- [Data Structures & Algorithms](#-data-structures--algorithms)
- [Module Overview](#-module-overview)
- [Requirements](#-requirements)

---

## ● Features

| Feature | Curses UI | Plain Terminal |
|---|:---:|:---:|
| Player vs Player | ✅ | ✅ |
| Player vs AI | ✅ | ✅ |
| 8×8 / 10×10 / 12×12 boards | ✅ | ✅ |
| Easy / Medium / Hard AI | ✅ | ✅ |
| Multi-jump chain captures | ✅ | ✅ |
| Forced capture enforcement | ✅ | ✅ |
| Undo / Redo history mode | ✅ | ✅ (AI mode only) |
| Per-player capture counter | ✅ | ✅ |
| Player name input | ✅ | ✅ |
| Countdown timer (per player) | ✅ | ❌ |
| Piece highlight & animations | ✅ | ❌ |
| King promotion | ✅ | ✅ |

---

## ○ Project Structure

```
checkers/
│
├── board.py          # Game state, rules, move generation, multi-jump chains
├── ai.py             # Minimax with alpha-beta pruning, board evaluation
├── curses_ui.py      # Curses-based terminal UI, history mode, animations
├── menu.py           # Curses interactive main menu
├── main.py           # Entry point for curses interface
├── main_plain.py     # Entry point for plain terminal interface
└── README.md
```

---

## ● How to Run

### Curses Interface (recommended)

```bash
python main.py
```

> **Windows users:** The curses interface requires the `windows-curses` package.
> Install it with:
> ```bash
> pip install windows-curses
> ```

### Plain Terminal Interface (no dependencies)

```bash
python main_plain.py
```

---

## ○ How to Play

Pieces move diagonally forward one square at a time. Captures are made by jumping over an opponent's piece to an empty square beyond it. A piece reaching the opponent's back row becomes a **King** (⬤ / ◯) and can move in both directions.

**Piece symbols:**

| Symbol | Meaning |
|---|---|
| `●` | Player piece |
| `⬤` | Player king |
| `○` | AI / opponent piece |
| `◯` | AI / opponent king |
| `·` | Empty square |

---

## ● Game Modes

### Player vs AI
Play against the minimax AI. Choose your difficulty:

| Difficulty | Search Depth | Strength |
|---|---|---|
| Easy | 2 | Looks 2 moves ahead |
| Medium | 3 | Looks 3 moves ahead |
| Hard | 4 | Looks 4 moves ahead |

### Player vs Player
Two players share the same terminal, taking turns.

### Board Sizes

| Size | Pieces per side | Notes |
|---|---|---|
| 8×8 | 12 | Standard checkers |
| 10×10 | 20 | International variant |
| 12×12 | 30 | Extended variant |

---

## ○ Controls

### Curses Interface

| Key | Action |
|---|---|
| `↑ ↓ ← →` | Move cursor |
| `Enter` | Select piece / confirm move |
| `u` | Enter history mode (AI mode only) |
| `q` | Quit |

**History Mode:**

| Key | Action |
|---|---|
| `u` | Undo (step back) |
| `r` | Redo (step forward) |
| `Enter` | Confirm and resume from here |
| `q` | Quit game |

### Plain Terminal Interface

Type coordinates as `row,col` (1-indexed). For example, `6,3` selects the piece at row 6, column 3.

| Input | Action |
|---|---|
| `row,col` | Select piece or move destination |
| `u` | Enter history mode (AI mode only) |
| `q` | Quit |

---

## ● Data Structures & Algorithms

### Data Structures

| Structure | Location | Purpose |
|---|---|---|
| 2D List | `board.py` | Board representation — O(1) cell access |
| Dictionary | `board.py` | Move map: position → valid moves |
| List (as stack) | `curses_ui.py`, `main_plain.py` | Undo/redo history |
| Set | `board.py` | Tracks captured squares during multi-jump chain discovery |
| Tuple | All files | Immutable positions and history entries |

### Algorithms

**Minimax with Alpha-Beta Pruning**  
The AI searches the game tree up to a configured depth. Alpha-beta pruning eliminates branches that cannot influence the final decision, reducing the worst-case complexity from O(b^d) to approximately O(b^(d/2)).

**Recursive Backtracking (`get_jump_chains`)**  
Finds all complete multi-jump capture chains from a piece. Simulates each hop, recurses from the landing square, then undoes the hop — a classic explore-then-restore pattern.

**Heuristic Evaluation (`evaluate_board`)**  
Scores each board position using piece value, king value, centre control, advancement, edge safety, and mobility (move count difference).

---

## ○ Module Overview

### `board.py`
Core game logic. No UI dependency — can be used independently.

- `Board.__init__` — builds the 2D grid and places starting pieces
- `setup_pieces` — places pieces symmetrically based on board size
- `get_moves` — returns valid non-capture moves for a piece
- `captures` — returns valid capture landing squares for a piece
- `get_all_moves` — returns all moves for a player; enforces forced capture
- `make_move` — executes and validates a single hop
- `make_move_no_validate` — fast internal hop used during chain simulation
- `get_jump_chains` — recursively finds all complete capture chains
- `get_all_jump_chains` — collects chains for all pieces of a player
- `check_winner` — returns winner or None
- `has_capture` — fast check if any capture is available

### `ai.py`
AI decision-making. No UI dependency.

- `evaluate_board` — heuristic board scorer
- `get_next_states` — generates all board states after one full turn (expands complete multi-jump chains)
- `minimax` — minimax with alpha-beta pruning; returns best score, move summary, and full chain

### `curses_ui.py`
Terminal UI using Python's `curses` library.

- `draw_board` — renders the full game screen each frame
- `run_curses_game` — main game loop with input handling, history, timers, and AI
- `animate_move` — flashes a piece between start and end positions
- `move_cursor` — updates cursor position from arrow key input
- `prompt_name` — collects player name via curses input
- `show_message` — overlays a temporary message on the board

### `menu.py`
Curses interactive main menu with arrow key navigation and forced capture toggle.

### `main.py`
Entry point for curses interface. Collects setup options and launches `run_curses_game`.

### `main_plain.py`
Entry point for plain terminal interface. No external dependencies beyond Python standard library.

- `player_turn_ai` — handles a human turn with history mode access
- `player_turn_pvp` — handles a human turn without history
- `run_game` — main game loop
- `history_mode` — interactive history browser for plain terminal

---

## ● Requirements

### Curses Interface
- Python 3.8+
- `windows-curses` (Windows only): `pip install windows-curses`

### Plain Terminal Interface
- Python 3.8+
- No additional packages required

---

## ○ Known Limitations

- The plain terminal version does not support timers (Python's `input()` is blocking)
- History mode in PVP is intentionally disabled — both players share the same screen, making undo potentially unfair
- The curses interface may not render correctly on terminals that do not support Unicode

---

*Built for SET08122 Algorithms and Data Structures — Edinburgh Napier University*
