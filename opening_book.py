"""
Opening Book
============
Pre-defined opening moves
"""

OPENINGS = {
    # Ruy Lopez
    "ruy_lopez": {
        "name": "Ruy Lopez",
        "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]
    },
    # Italian Game
    "italian": {
        "name": "Italian Game",
        "moves": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"]
    },
    # Sicilian Defense
    "sicilian": {
        "name": "Sicilian Defense",
        "moves": ["e2e4", "c7c5"]
    },
    # French Defense
    "french": {
        "name": "French Defense",
        "moves": ["e2e4", "e7e6"]
    },
    # Caro-Kann
    "caro_kann": {
        "name": "Caro-Kann Defense",
        "moves": ["e2e4", "c7c6"]
    },
    # Queen's Gambit
    "queens_gambit": {
        "name": "Queen's Gambit",
        "moves": ["d2d4", "d7d5", "c2c4"]
    },
    # King's Gambit
    "kings_gambit": {
        "name": "King's Gambit",
        "moves": ["e2e4", "e7e5", "f2f4"]
    },
    # English Opening
    "english": {
        "name": "English Opening",
        "moves": ["c2c4"]
    }
}


class OpeningBook:
    """Opening book for chess"""
    
    def __init__(self):
        self.openings = OPENINGS
    
    def get_opening(self, key):
        """Get opening by key"""
        return self.openings.get(key)
    
    def find_opening(self, moves):
        """Find matching opening"""
        move_str = " ".join(moves)
        
        for key, opening in self.openings.items():
            opening_moves = " ".join(opening["moves"][:len(moves)])
            if move_str.startswith(opening_moves):
                return opening
        
        return None
    
    def list_openings(self):
        """List all available openings"""
        return list(self.openings.keys())


# Example usage
if __name__ == "__main__":
    book = OpeningBook()
    print("Available openings:")
    for key in book.list_openings():
        opening = book.get_opening(key)
        print(f"  {key}: {opening['name']}")
        print(f"    Moves: {' '.join(opening['moves'])}")
