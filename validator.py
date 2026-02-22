"""
Move Validator
=============
Validates chess moves according to rules
"""

from pieces import Pawn, Knight, Bishop, Rook, Queen, King


class MoveValidator:
    """Validates chess moves"""
    
    def __init__(self, board):
        self.board = board
    
    def is_valid_move(self, from_row, from_col, to_row, to_col, color):
        """Check if move is valid"""
        piece = self.board.get_piece(from_row, from_col)
        
        if not piece:
            return False, "No piece at starting position"
        
        if piece.color != color:
            return False, "Cannot move enemy piece"
        
        # Check basic movement rules
        valid, reason = self._check_piece_movement(piece, from_row, from_col, to_row, to_col)
        if not valid:
            return False, reason
        
        # Check if path is clear
        if not self._is_path_clear(from_row, from_col, to_row, to_col):
            return False, "Path is not clear"
        
        # Check if king would be in check after move
        if self._would_be_in_check(from_row, from_col, to_row, to_col, color):
            return False, "King would be in check"
        
        return True, "Valid move"
    
    def _check_piece_movement(self, piece, from_row, from_col, to_row, to_col):
        """Check if piece can move to target"""
        dr = to_row - from_row
        dc = to_col - from_col
        
        if isinstance(piece, Pawn):
            direction = -1 if piece.color == 'white' else 1
            start_row = 6 if piece.color == 'white' else 1
            
            # Forward move
            if dc == 0:
                if dr == direction and self.board.is_empty(to_row, to_col):
                    return True, "Valid"
                if dr == 2 * direction and from_row == start_row:
                    if self.board.is_empty(to_row, to_col) and self.board.is_empty(from_row + direction, to_col):
                        return True, "Valid"
            # Capture
            elif abs(dc) == 1 and dr == direction:
                if self.board.is_enemy(to_row, to_col, piece.color):
                    return True, "Valid"
            
            return False, "Invalid pawn move"
        
        if isinstance(piece, Knight):
            if (abs(dr) == 2 and abs(dc) == 1) or (abs(dr) == 1 and abs(dc) == 2):
                target = self.board.get_piece(to_row, to_col)
                if not target or target.color != piece.color:
                    return True, "Valid"
            return False, "Invalid knight move"
        
        if isinstance(piece, Bishop):
            if abs(dr) == abs(dc):
                return True, "Valid"
            return False, "Invalid bishop move"
        
        if isinstance(piece, Rook):
            if dr == 0 or dc == 0:
                return True, "Valid"
            return False, "Invalid rook move"
        
        if isinstance(piece, Queen):
            if dr == 0 or dc == 0 or abs(dr) == abs(dc):
                return True, "Valid"
            return False, "Invalid queen move"
        
        if isinstance(piece, King):
            if abs(dr) <= 1 and abs(dc) <= 1:
                target = self.board.get_piece(to_row, to_col)
                if not target or target.color != piece.color:
                    return True, "Valid"
            return False, "Invalid king move"
        
        return False, "Unknown piece"
    
    def _is_path_clear(self, from_row, from_col, to_row, to_col):
        """Check if path is clear for sliding pieces"""
        piece = self.board.get_piece(from_row, from_col)
        
        # Non-sliding pieces don't need path check
        if isinstance(piece, (Pawn, Knight, King)):
            return True
        
        dr = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        dc = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        row, col = from_row + dr, from_col + dc
        while (row, col) != (to_row, to_col):
            if not self.board.is_empty(row, col):
                return False
            row += dr
            col += dc
        
        return True
    
    def _would_be_in_check(self, from_row, from_col, to_row, to_col, color):
        """Check if move would leave king in check"""
        # Make move temporarily
        piece = self.board.get_piece(from_row, from_col)
        captured = self.board.get_piece(to_row, to_col)
        
        self.board.set_piece(to_row, to_col, piece)
        self.board.remove_piece(from_row, from_col)
        
        in_check = self.board.is_in_check(color)
        
        # Undo move
        self.board.set_piece(from_row, from_col, piece)
        self.board.set_piece(to_row, to_col, captured)
        
        return in_check
    
    def get_valid_moves(self, row, col, color):
        """Get all valid moves for piece at position"""
        piece = self.board.get_piece(row, col)
        if not piece or piece.color != color:
            return []
        
        valid_moves = []
        for to_row in range(8):
            for to_col in range(8):
                if (to_row, to_col) != (row, col):
                    valid, _ = self.is_valid_move(row, col, to_row, to_col, color)
                    if valid:
                        valid_moves.append((to_row, to_col))
        
        return valid_moves
