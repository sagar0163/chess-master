# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-22

### Added
- Complete chess game implementation
- AI opponent with minimax algorithm and alpha-beta pruning
- Terminal UI with Unicode chess pieces
- Move validation for all piece types
- Special moves: castling, en passant, pawn promotion
- Game history tracking and analysis
- Opening book with common openings
- Configuration system
- Position evaluation
- Game statistics

### Features
- Full legal move generation
- Check and checkmate detection
- Stalemate detection
- Multiple difficulty levels
- Position analysis
- Move suggestions

### Components
- pieces.py - Piece definitions
- board.py - Board representation
- validator.py - Move validation
- ai.py - AI engine
- display.py - Terminal UI
- game.py - Main game logic
- history.py - Game history & analysis
- special_moves.py - Special move handling
- opening_book.py - Opening repertoire
- config_loader.py - Configuration management
- utils.py - Utility functions
