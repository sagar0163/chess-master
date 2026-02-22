"""
Chess Piece Definitions
======================
"""

class Piece:
    """Base piece class"""
    
    def __init__(self, color, symbol):
        self.color = color  # 'white' or 'black'
        self.symbol = symbol
        self.has_moved = False
    
    def __repr__(self):
        return self.symbol
    
    def get_value(self):
        return 0


class King(Piece):
    def __init__(self, color):
        symbol = '♔' if color == 'white' else '♚'
        super().__init__(color, symbol)
    
    def get_value(self):
        return 100


class Queen(Piece):
    def __init__(self, color):
        symbol = '♕' if color == 'white' else '♛'
        super().__init__(color, symbol)
    
    def get_value(self):
        return 9


class Rook(Piece):
    def __init__(self, color):
        symbol = '♖' if color == 'white' else '♜'
        super().__init__(color, symbol)
    
    def get_value(self):
        return 5


class Bishop(Piece):
    def __init__(self, color):
        symbol = '♗' if color == 'white' else '♝'
        super().__init__(color, symbol)
    
    def get_value(self):
        return 3


class Knight(Piece):
    def __init__(self, color):
        symbol = '♘' if color == 'white' == 'white' else '♞'
        super().__init__(color, symbol)
    
    def get_value(self):
        return 3


class Pawn(Piece):
    def __init__(self, color):
        symbol = '♙' if color == 'white' else '♟'
        super().__init__(color, symbol)
    
    def get_value(self):
        return 1
