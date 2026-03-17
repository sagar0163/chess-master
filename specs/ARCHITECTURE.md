# Architecture Document: Chess Master

## 1. System Overview

Chess Master is a Python-based command-line chess game. It follows a modular design, separating core game logic, AI, move validation, and display into distinct components. The system operates within a standard game loop, handling user input, updating game state, and rendering the board.

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Main Game Loop                         │
│                      (main.py)                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    ▼                 ▼                 ▼
┌─────────┐     ┌───────────┐     ┌──────────┐
│  Config │     │  Game     │     │ Display  │
│  Loader │     │  Logic    │     │ (Terminal)│
└─────────┘     └───────────┘     └──────────┘
    │                 │                 │
    │                 ▼                 │
    │          ┌───────────┐            │
    │          │  Board    │            │
    │          │  Manager  │            │
    │          └───────────┘            │
    │                 │                 │
    │                 ▼                 │
    │          ┌───────────┐            │
    │          │  Move     │            │
    │          │  Validator│            │
    │          └───────────┘            │
    │                 │                 │
    │                 ▼                 │
    │          ┌───────────┐            │
    │          │    AI     │            │
    │          │  Engine   │            │
    │          └───────────┘            │
    │                                   │
    └───────────────────────────────────┘
```

## 3. Core Components

### 3.1 Game Logic (game.py)
- Manages game state (current turn, game over)
- Integrates move validation, AI, and display
- Handles player input and applies moves

### 3.2 Board Manager (board.py)
- Represents the 8x8 chess board (e.g., 2D array)
- Manages piece positions
- Handles piece movement and captures

### 3.3 Piece Definitions (pieces.py)
- Defines properties and movement rules for each chess piece (Pawn, Rook, Knight, Bishop, Queen, King)

### 3.4 Move Validator (validator.py)
- Checks if a proposed move is legal according to chess rules
- Considers piece movement, board state, checks, and checkmates
- Handles special moves: castling, en passant, pawn promotion

### 3.5 AI Engine (ai.py)
- Implements the Minimax algorithm with Alpha-Beta Pruning
- Evaluates board positions to determine optimal moves
- Configurable search depth for difficulty adjustment

### 3.6 Display (display.py)
- Renders the current board state to the terminal
- Uses Unicode characters for chess pieces
- Provides clear text output for game information (turn, status)

### 3.7 Game History (history.py)
- Records all moves made in a game
- Supports saving and loading game states

### 3.8 Opening Book (opening_book.py)
- Stores a collection of common chess openings
- AI uses this to make early game moves

### 3.9 Configuration (config_loader.py, config.json)
- Loads game settings from `config.json` (e.g., AI difficulty)

## 4. Data Flow

```
User Input (Move) → Move Validator → Game Logic → AI Engine (if AI turn) → Board Manager → Display → User Output
```

## 5. Game Loop

```
┌─────────────────────────────────────────┐
│               Game Loop                 │
├─────────────────────────────────────────┤
│ 1. Initialize Game                      │
│    - Load config, board, pieces         │
│    - Display initial board              │
│                                         │
│ 2. Loop Until Game Over                 │
│    a. Get Player/AI Move                │
│       - If Human: Read input           │
│       - If AI: Calculate move           │
│                                         │
│    b. Validate Move                     │
│       - Check legality, check/mate      │
│                                         │
│    c. Apply Move                       │
│       - Update board, piece positions   │
│       - Record in history               │
│                                         │
│    d. Render Board & Info              │
│       - Clear screen, draw board, status│
│                                         │
│    e. Switch Turn                       │
│                                         │
│ 3. End Game                            │
│    - Display winner/draw, final state   │
└─────────────────────────────────────────┘
```

## 6. File Structure

```
chess-master/
├── main.py             # Entry point
├── game.py             # Main game logic
├── board.py            # Board representation
├── pieces.py           # Piece definitions
├── validator.py        # Move validation
├── ai.py               # AI engine
├── display.py          # Terminal UI rendering
├── history.py          # Game history management
├── special_moves.py    # Special chess moves logic
├── opening_book.py     # Chess opening library
├── config_loader.py    # Configuration loading
├── utils.py            # Utility functions
├── config.json         # Game settings
├── specs/              # Documentation
└── README.md
```

## 7. Dependencies

| Package | Purpose |
|---------|---------|
| Python 3.7+ | Runtime |
| (Standard Library) | OS, time, json |

---

*Document Version: 1.0*  
*Created: 2026-03-17*
