# Chess Master

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/python-3.7+-green" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License">
</p>

Expert-level chess game with AI opponent, written in Python.

## Features

- 🤖 **AI Opponent** - Minimax algorithm with alpha-beta pruning
- 🎨 **Beautiful UI** - Unicode chess pieces in terminal
- 📊 **Game Analysis** - Position evaluation and move suggestions
- 📚 **Opening Book** - Common chess openings
- 💾 **Game History** - Track and save games
- ⚙️ **Customizable** - Configurable difficulty and settings

## Installation

```bash
# Clone the repository
git clone https://github.com/sagar0163/chess-master.git
cd chess-master

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Usage

```bash
# Play against AI (default)
python main.py

# Play without AI (two players)
python main.py --no-ai

# Set AI difficulty (1-5)
python main.py --depth=4
```

## Controls

Enter moves in algebraic notation:
- `e2e4` - Move piece from e2 to e4
- `g1f3` - Knight from g1 to f3
- `a7a8q` - Pawn promotion to queen

## Project Structure

```
chess-master/
├── pieces.py         # Piece definitions
├── board.py          # Board representation
├── validator.py      # Move validation
├── ai.py            # AI engine
├── display.py       # Terminal UI
├── game.py         # Main game logic
├── history.py      # Game history
├── special_moves.py # Castling, en passant
├── opening_book.py # Opening repertoire
├── config_loader.py # Configuration
├── utils.py        # Utilities
├── main.py         # Entry point
└── config.json     # Settings
```

## License

MIT License - see LICENSE file for details.
