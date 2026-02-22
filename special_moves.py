"""
Special Moves Handler
=====================
Castling, en passant, and pawn promotion
"""

from pieces import King, Queen, Rook, Bishop, Knight, Pawn


class SpecialMoves:
    """Handle special chess moves"""
    
    def __init__(self, board):
        self.board = board
    
    def can_castle_kingside(self, color):
        """Check if kingside castling is possible"""
        if color == 'white':
            # King and rook haven't moved
            king = self.board.get_piece(7, 4)
            rook = self.board.get_piece(7, 7)
            
            if not king or not isinstance(king, King) or king.has_moved:
                return False
            if not rook or not isinstance(rook, Rook) or rook.has_moved:
                return False
            
            # Path must be clear
            if not self.board.is_empty(7, 5) or not self.board.is_empty(7, 6):
                return False
            
            # King can't be in check
            if self.board.is_in_check('white'):
                return False
            
            # Can't pass through check
            if self._square_under_attack(7, 5, 'white') or self._square_under_attack(7, 6, 'white'):
                return False
            
            return True
        else:
            king = self.board.get_piece(0, 4)
            rook = self.board.get_piece(0, 7)
            
            if not king or not isinstance(king, King) or king.has_moved:
                return False
            if not rook or not isinstance(rook, Rook) or rook.has_moved:
                return False
            
            if not self.board.is_empty(0, 5) or not self.board.is_empty(0, 6):
                return False
            
            if self.board.is_in_check('black'):
                return False
            
            if self._square_under_attack(0, 5, 'black') or self._square_under_attack(0, 6, 'black'):
                return False
            
            return True
    
    def can_castle_queenside(self, color):
        """Check if queenside castling is possible"""
        if color == 'white':
            king = self.board.get_piece(7, 4)
            rook = self.board.get_piece(7, 0)
            
            if not king or not isinstance(king, King) or king.has_moved:
                return False
            if not rook or not isinstance(rook, Rook) or rook.has_moved:
                return False
            
            # Path must be clear
            if not self.board.is_empty(7, 1) or not self.board.is_empty(7, 2) or not self.board.is_empty(7, 3):
                return False
            
            if self.board.is_in_check('white'):
                return False
            
            if self._square_under_attack(7, 2, 'white') or self._square_under_attack(7, 3, 'white'):
                return False
            
            return True
        else:
            king = self.board.get_piece(0, 4)
            rook = self.board.get_piece(0, 0)
            
            if not king or not isinstance(king, King) or king.has_moved:
                return False
            if not rook or not isinstance(rook, Rook) or rook.has_moved:
                return False
            
            if not self.board.is_empty(0, 1) or not self.board.is_empty(0, 2) or not self.board.is_empty(0, 3):
                return False
            
            if self.board.is_in_check('black'):
                return False
            
            if self._square_under_attack(0, 2, 'black') or self._square_under_attack(0, 3, 'black'):
                return False
            
            return True
    
    def do_castle(self, color, kingside=True):
        """Perform castling move"""
        if color == 'white':
            row = 7
            if kingside:
                # Move king
                king = self.board.get_piece(row, 4)
                self.board.set_piece(row, 6, king)
                self.board.remove_piece(row, 4)
                king.has_moved = True
                
                # Move rook
                rook = self.board.get_piece(row, 7)
                self.board.set_piece(row, 5, rook)
                self.board.remove_piece(row, 7)
                rook.has_moved = True
            else:
                king = self.board.get_piece(row, 4)
                self.board.set_piece(row, 2, king)
                self.board.remove_piece(row, 4)
                king.has_moved = True
                
                rook = self.board.get_piece(row, 0)
                self.board.set_piece(row, 3, rook)
                self.board.remove_piece(row, 0)
                rook.has_moved = True
        else:
            row = 0
            if kingside:
                king = self.board.get_piece(row, 4)
                self.board.set_piece(row, 6, king)
                self.board.remove_piece(row, 4)
                king.has_moved = True
                
                rook = self.board.get_piece(row, 7)
                self.board.set_piece(row, 5, rook)
                self.board.remove_piece(row, 7)
                rook.has_moved = True
            else:
                king = self.board.get_piece(row, 4)
                self.board.set_piece(row, 2, king)
                self.board.remove_piece(row, 4)
                king.has_moved = True
                
                rook = self.board.get_piece(row, 0)
                self.board.set_piece(row, 3, rook)
                self.board.remove_piece(row, 0)
                rook.has_moved = True
    
    def can_en_passant(self, color, from_pos, to_pos):
        """Check if en passant is possible"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board.get_piece(from_row, from_col)
        
        if not isinstance(piece, Pawn):
            return False
        
        # Must be pawn moving diagonally
        if abs(to_col - from_col) != 1 or abs(to_row - from_row) != 1:
            return False
        
        # Target must be empty
        if not self.board.is_empty(to_row, to_col):
            return False
        
        # Check if pawn just moved two squares
        direction = -1 if color == 'white' else 1
        if from_row != (6 if color == 'white' else 1):
            return False
        
        expected_row = from_row + 2 * direction
        if to_row != expected_row:
            return False
        
        # Check adjacent pawn
        adjacent_row = from_row
        adjacent_col = to_col
        adjacent_piece = self.board.get_piece(adjacent_row, adjacent_col)
        
        if not adjacent_piece or not isinstance(adjacent_piece, Pawn):
            return False
        
        if adjacent_piece.color == color:
            return False
        
        # Check if adjacent pawn just moved two squares
        if len(self.board.move_history) < 1:
            return False
        
        last_move = self.board.move_history[-1]
        if last_move['piece'] != adjacent_piece:
            return False
        
        last_from = last_move['from']
        last_to = last_move['to']
        
        expected_from = 1 if adjacent_piece.color == 'white' else 6
        expected_to = 3 if adjacent_piece.color == 'white' else 4
        
        if last_from[0] != expected_from or last_to[0] != expected_to:
            return False
        
        return True
    
    def do_en_passant(self, from_row, from_col, to_row, to_col):
        """Perform en passant capture"""
        # Move the pawn
        piece = self.board.get_piece(from_row, from_col)
        self.board.set_piece(to_row, to_col, piece)
        self.board.remove_piece(from_row, from_col)
        
        # Capture the pawn behind
        capture_row = from_row
        capture_col = to_col
        self.board.remove_piece(capture_row, capture_col)
    
    def can_promote(self, row, col):
        """Check if pawn can promote"""
        piece = self.board.get_piece(row, col)
        
        if not isinstance(piece, Pawn):
            return False
        
        # Must be on last rank
        if piece.color == 'white' and row == 0:
            return True
        if piece.color == 'black' and row == 7:
            return True
        
        return False
    
    def do_promotion(self, row, col, promotion_piece):
        """Promote pawn"""
        piece = self.board.get_piece(row, col)
        
        promotion_map = {
            'queen': Queen,
            'rook': Rook,
            'bishop': Bishop,
            'knight': Knight
        }
        
        piece_class = promotion_map.get(promotion_piece.lower(), Queen)
        self.board.set_piece(row, col, piece_class(piece.color))
    
    def _square_under_attack(self, row, col, color):
        """Check if square is under attack"""
        enemy_color = 'black' if color == 'white' else 'white'
        
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(r, c)
                if piece and piece.color == enemy_color:
                    if self.board._can_attack(r, c, row, col, enemy_color):
                        return True
        
        return False
