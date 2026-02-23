"""
Chess Board Display
==================
Terminal UI for chess game
"""


class ChessDisplay:
    """Display chess board in terminal"""
    
    def __init__(self):
        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    def display(self, board):
        """Display the chess board"""
        print("\n" + " " * 4 + "  ".join(self.files))
        print("  " + "━" * 17)
        
        for row in range(8):
            print(f"{8 - row} ", end="")
            
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    display = piece.symbol
                else:
                    # Checkerboard pattern
                    display = "·" if (row + col) % 2 == 0 else " "
                
                print(f" {display}", end="")
            
            print(f" {8 - row}")
        
        print("  " + "━" * 17)
        print(" " * 4 + "  ".join(self.files) + "\n")
    
    def display_with_indicators(self, board, valid_moves=None, last_move=None):
        """Display board with move indicators"""
        print("\n" + " " * 4 + "  ".join(self.files))
        print("  " + "━" * 17)
        
        for row in range(8):
            print(f"{8 - row} ", end="")
            
            for col in range(8):
                piece = board.get_piece(row, col)
                
                # Check if this is a valid move target
                is_valid = valid_moves and (row, col) in valid_moves
                
                # Check if this is last move
                is_last = False
                if last_move:
                    is_last = (row, col) == last_move[0] or (row, col) == last_move[1]
                
                if piece:
                    display = piece.symbol
                elif is_valid:
                    display = "•"
                else:
                    display = "·" if (row + col) % 2 == 0 else " "
                
                # Add markers
                if is_last:
                    display = f"[{display}]" if len(display) == 1 else display
                elif is_valid:
                    display = f"({display})" if len(display) == 1 else display
                
                print(f" {display}", end="")
            
            print(f" {8 - row}")
        
        print("  " + "━" * 17)
        print(" " * 4 + "  ".join(self.files) + "\n")
    
    def show_captured(self, board):
        """Show captured pieces"""
        white_captured = []
        black_captured = []
        
        for move in board.move_history:
            captured = move.get('captured')
            if captured:
                if captured.color == 'white':
                    white_captured.append(captured.symbol)
                else:
                    black_captured.append(captured.symbol)
        
        print("Captured by White:", " ".join(black_captured) if black_captured else "None")
        print("Captured by Black:", " ".join(white_captured) if white_captured else "None")
    
    def show_move_history(self, board, last_n=10):
        """Show recent moves"""
        history = board.move_history[-last_n:]
        
        print("\nRecent Moves:")
        for i, move in enumerate(history):
            piece = move['piece']
            from_pos = self._pos_to_algebraic(move['from'])
            to_pos = self._pos_to_algebraic(move['to'])
            symbol = piece.symbol
            
            print(f"{len(board.move_history) - len(history) + i + 1}. {symbol}: {from_pos} → {to_pos}")
    
    def _pos_to_algebraic(self, pos):
        """Convert position to algebraic notation"""
        row, col = pos
        return f"{self.files[col]}{8 - row}"
    
    def get_move_input(self, turn):
        """Get move from player"""
        prompt = f"{turn.capitalize()}'s move (e.g., e2e4): "
        move = input(prompt).strip().lower()
        
        # Parse move
        if len(move) == 4:
            try:
                from_pos = move[:2]
                to_pos = move[2:]
                
                from_col = ord(from_pos[0]) - ord('a')
                from_row = 8 - int(from_pos[1])
                
                to_col = ord(to_pos[0]) - ord('a')
                to_row = 8 - int(to_pos[1])
                
                return (from_row, from_col), (to_row, to_col)
            except:
                pass
        
        return None
    
    def show_status(self, board, turn):
        """Show game status"""
        print(f"\nTurn: {turn.capitalize()}")
        
        if board.is_in_check('white'):
            print("⚠ White is in CHECK!")
        
        if board.is_in_check('black'):
            print("⚠ Black is in CHECK!")
    
    def show_turn_indicator(self, turn):
        """Show whose turn it is"""
        color = "⚪ White" if turn == 'white' else "⚫ Black"
        print(f"\n{'='*40}")
        print(f"  {color} to move")
        print(f"{'='*40}\n")


class ChessBoardDisplay:
    """Web-friendly board display helper"""
    
    def __init__(self):
        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    def get_piece_unicode(self, piece):
        """Get Unicode symbol for piece"""
        symbols = {
            ('king', 'white'): '♔', ('king', 'black'): '♚',
            ('queen', 'white'): '♕', ('queen', 'black'): '♛',
            ('rook', 'white'): '♖', ('rook', 'black'): '♜',
            ('bishop', 'white'): '♗', ('bishop', 'black'): '♝',
            ('knight', 'white'): '♘', ('knight', 'black'): '♞',
            ('pawn', 'white'): '♙', ('pawn', 'black'): '♟'
        }
        return symbols.get((piece.__class__.__name__.lower(), piece.color), '')
