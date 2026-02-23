"""
Chess Board Representation
=========================
"""

from pieces import King, Queen, Rook, Bishop, Knight, Pawn


class ChessBoard:
    """8x8 Chess board representation"""
    
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = 'white'
        self.move_history = []
        self.setup_initial_position()
    
    def setup_initial_position(self):
        """Set up the initial chess position"""
        # Back row pieces
        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        for col, piece_class in enumerate(back_rank):
            self.board[0][col] = piece_class('black')
            self.board[7][col] = piece_class('white')
        
        # Pawns
        for col in range(8):
            self.board[1][col] = Pawn('black')
            self.board[6][col] = Pawn('white')
    
    def get_piece(self, row, col):
        """Get piece at position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def set_piece(self, row, col, piece):
        """Set piece at position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
    
    def remove_piece(self, row, col):
        """Remove piece from position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = None
    
    def is_empty(self, row, col):
        """Check if position is empty"""
        return self.get_piece(row, col) is None
    
    def is_enemy(self, row, col, color):
        """Check if position has enemy piece"""
        piece = self.get_piece(row, col)
        return piece is not None and piece.color != color
    
    def in_bounds(self, row, col):
        """Check if position is on board"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Make a move on the board"""
        piece = self.get_piece(from_row, from_col)
        if piece:
            captured = self.get_piece(to_row, to_col)
            self.set_piece(to_row, to_col, piece)
            self.remove_piece(from_row, from_col)
            piece.has_moved = True
            
            # Record move
            self.move_history.append({
                'from': (from_row, from_col),
                'to': (to_row, to_col),
                'piece': piece,
                'captured': captured
            })
            
            return True
        return False
    
    def undo_move(self):
        """Undo the last move"""
        if self.move_history:
            move = self.move_history.pop()
            from_row, from_col = move['from']
            to_row, to_col = move['to']
            piece = self.get_piece(to_row, to_col)
            
            self.set_piece(from_row, from_col, piece)
            self.remove_piece(to_row, to_col)
            
            if move['captured']:
                self.set_piece(to_row, to_col, move['captured'])
            
            return True
        return False
    
    def get_all_pieces(self, color):
        """Get all pieces of a given color"""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    pieces.append((row, col, piece))
        return pieces
    
    def is_in_check(self, color):
        """Check if king of given color is in check"""
        # Find king
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
        
        if not king_pos:
            return False
        
        # Check if any enemy can attack king
        enemy_color = 'black' if color == 'white' else 'white'
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == enemy_color:
                    if self._can_attack(row, col, king_pos[0], king_pos[1], enemy_color):
                        return True
        
        return False
    
    def _can_attack(self, from_row, from_col, to_row, to_col, color):
        """Check if piece can attack position"""
        piece = self.get_piece(from_row, from_col)
        if not piece:
            return False
        
        # Simplified attack detection
        if isinstance(piece, Pawn):
            direction = -1 if color == 'white' else 1
            return (from_row + direction == to_row and 
                    abs(from_col - to_col) == 1)
        
        if isinstance(piece, Knight):
            dr = abs(from_row - to_row)
            dc = abs(from_col - to_col)
            return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)
        
        if isinstance(piece, Bishop):
            if abs(from_row - to_row) == abs(from_col - to_col):
                return self._clear_path(from_row, from_col, to_row, to_col)
        
        if isinstance(piece, Rook):
            if from_row == to_row or from_col == to_col:
                return self._clear_path(from_row, from_col, to_row, to_col)
        
        if isinstance(piece, Queen):
            if (from_row == to_row or from_col == to_col or
                abs(from_row - to_row) == abs(from_col - to_col)):
                return self._clear_path(from_row, from_col, to_row, to_col)
        
        if isinstance(piece, King):
            return abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1
        
        return False
    
    def _clear_path(self, from_row, from_col, to_row, to_col):
        """Check if path is clear for sliding pieces"""
        dr = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        dc = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        row, col = from_row + dr, from_col + dc
        while (row, col) != (to_row, to_col):
            if not self.is_empty(row, col):
                return False
            row += dr
            col += dc
        
        return True
    
    def get_board_state(self):
        """Get board state as 2D array for frontend"""
        state = []
        
        for row in range(8):
            row_state = []
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    row_state.append({
                        'type': piece.__class__.__name__.lower(),
                        'color': piece.color
                    })
                else:
                    row_state.append(None)
            state.append(row_state)
        return state
    
    def to_fen(self):
        """Convert board to FEN notation"""
        fen_rows = []
        
        for row in range(8):
            empty_count = 0
            fen_row = ""
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    symbol = piece.__class__.__name__[0].upper()
                    if piece.color == 'black':
                        symbol = symbol.lower()
                    else:
                        symbol = symbol.upper()
                    fen_row += symbol
            
            if empty_count > 0:
                fen_row += str(empty_count)
            
            fen_rows.append(fen_row)
        
        turn = self.current_turn[0].upper()
        
        return '/'.join(fen_rows) + f' {turn} - - 0 1'
