"""
Utilities Module
===============
Helper functions for chess game
"""


def algebraic_to_coords(pos):
    """Convert algebraic notation to coordinates"""
    if len(pos) != 2:
        return None
    
    col = ord(pos[0].lower()) - ord('a')
    row = 8 - int(pos[1])
    
    if 0 <= col <= 7 and 0 <= row <= 7:
        return (row, col)
    return None


def coords_to_algebraic(row, col):
    """Convert coordinates to algebraic notation"""
    file_char = chr(ord('a') + col)
    rank = 8 - row
    return f"{file_char}{rank}"


def parse_move(move_str):
    """Parse move string to coordinates"""
    if len(move_str) == 4:
        from_pos = algebraic_to_coords(move_str[:2])
        to_pos = algebraic_to_coords(move_str[2:])
        
        if from_pos and to_pos:
            return from_pos, to_pos
    
    return None


def format_time(seconds):
    """Format time in seconds to human readable"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def get_piece_symbol(piece_type, color):
    """Get Unicode symbol for piece"""
    pieces = {
        'king': '♔' if color == 'white' else '♚',
        'queen': '♕' if color == 'white' else '♛',
        'rook': '♖' if color == 'white' else '♜',
        'bishop': '♗' if color == 'white' else '♝',
        'knight': '♘' if color == 'white' else '♞',
        'pawn': '♙' if color == 'white' else '♟'
    }
    return pieces.get(piece_type.lower(), '?')


def is_checkmate(board, color):
    """Check if position is checkmate"""
    if not board.is_in_check(color):
        return False
    
    # Check if any move escapes check
    from validator import MoveValidator
    validator = MoveValidator(board)
    
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and piece.color == color:
                moves = validator.get_valid_moves(row, col, color)
                if moves:
                    return False
    
    return True


def is_stalemate(board, color):
    """Check if position is stalemate"""
    if board.is_in_check(color):
        return False
    
    from validator import MoveValidator
    validator = MoveValidator(board)
    
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and piece.color == color:
                moves = validator.get_valid_moves(row, col, color)
                if moves:
                    return False
    
    return True
