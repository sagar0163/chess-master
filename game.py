"""
Chess Game Engine
=================
Main game logic and state management
"""

from board import ChessBoard
from validator import MoveValidator
from ai import ChessAI
from display import ChessDisplay
import os


class ChessGame:
    """Main chess game class"""
    
    def __init__(self, ai_enabled=True, ai_depth=3):
        self.board = ChessBoard()
        self.validator = MoveValidator(self.board)
        self.display = ChessDisplay()
        self.ai_enabled = ai_enabled
        self.ai = ChessAI(depth=ai_depth) if ai_enabled else None
        self.game_over = False
        self.winner = None
        self.last_move = None
    
    def start(self):
        """Start the game"""
        print("♟♟♟ CHESS MASTER ♟♟♟")
        print("=" * 40)
        print("Expert-level chess with AI opponent")
        print("=" * 40)
        
        if self.ai_enabled:
            print(f"AI enabled (depth: {self.ai.depth})")
        
        print("\nEnter moves in algebraic notation:")
        print("Example: e2e4, g1f3, a7a8q (for promotion)")
        print()
        
        self.game_loop()
    
    def game_loop(self):
        """Main game loop"""
        while not self.game_over:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display board
            self.display.display(self.board)
            
            # Show status
            self.display.show_status(self.board, self.board.current_turn)
            
            # Check for game over
            if self._check_game_over():
                break
            
            # Get move
            if self.board.current_turn == 'white' or not self.ai_enabled:
                self._player_move()
            else:
                self._ai_move()
            
            # Switch turns
            self.board.current_turn = 'black' if self.board.current_turn == 'white' else 'white'
        
        # Game over
        self._end_game()
    
    def _player_move(self):
        """Handle player move"""
        valid_move = False
        attempts = 0
        
        while not valid_move and attempts < 3:
            move = self.display.get_move_input(self.board.current_turn)
            
            if not move:
                print("Invalid format. Use: e2e4")
                attempts += 1
                continue
            
            from_pos, to_pos = move
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            # Check valid move
            valid, reason = self.validator.is_valid_move(
                from_row, from_col, to_row, to_col,
                self.board.current_turn
            )
            
            if valid:
                self.board.make_move(from_row, from_col, to_row, to_col)
                self.last_move = (from_pos, to_pos)
                valid_move = True
            else:
                print(f"Invalid move: {reason}")
                attempts += 1
        
        if not valid_move:
            print("Using random valid move...")
            self._make_random_move()
    
    def _ai_move(self):
        """Handle AI move"""
        print(f"\nAI ({self.board.current_turn}) is thinking...")
        
        move = self.ai.get_best_move(self.board, self.board.current_turn)
        
        if move:
            from_pos, to_pos = move
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            self.board.make_move(from_row, from_col, to_row, to_col)
            self.last_move = (from_pos, to_pos)
            
            print(f"AI plays: {self._to_algebraic(from_pos)} → {self._to_algebraic(to_pos)}")
            print(f"Nodes evaluated: {self.ai.nodes_evaluated}")
        else:
            print("AI has no valid moves!")
    
    def _make_random_move(self):
        """Make a random valid move"""
        import random
        
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == self.board.current_turn:
                    valid_moves = self.validator.get_valid_moves(row, col, self.board.current_turn)
                    for to_row, to_col in valid_moves:
                        moves.append(((row, col), (to_row, to_col)))
        
        if moves:
            move = random.choice(moves)
            from_pos, to_pos = move
            self.board.make_move(from_pos[0], from_pos[1], to_pos[0], to_pos[1])
            self.last_move = move
    
    def _check_game_over(self):
        """Check if game is over"""
        color = self.board.current_turn
        has_moves = False
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    moves = self.validator.get_valid_moves(row, col, color)
                    if moves:
                        has_moves = True
                        break
        
        if not has_moves:
            self.game_over = True
            if self.board.is_in_check(color):
                self.winner = 'black' if color == 'white' else 'white'
                print(f"\n{'#' * 40}")
                print(f"  CHECKMATE! {self.winner.capitalize()} wins!")
                print(f"{'#' * 40}")
            else:
                print("\nSTALEMATE! Game is a draw.")
            return True
        
        return False
    
    def _end_game(self):
        """Handle game end"""
        self.display.display(self.board)
        
        print("\n" + "=" * 40)
        print("GAME OVER")
        print("=" * 40)
        print(f"Total moves: {len(self.board.move_history)}")
        
        if self.winner:
            print(f"Winner: {self.winner.capitalize()}")
        else:
            print("Result: Draw")
    
    def _to_algebraic(self, pos):
        """Convert position to algebraic notation"""
        row, col = pos
        return f"{self.display.files[col]}{8 - row}"


if __name__ == "__main__":
    import sys
    
    ai_enabled = '--no-ai' not in sys.argv
    ai_depth = 3
    
    for arg in sys.argv:
        if arg.startswith('--depth='):
            ai_depth = int(arg.split('=')[1])
    
    game = ChessGame(ai_enabled=ai_enabled, ai_depth=ai_depth)
    game.start()
