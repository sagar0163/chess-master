"""
Game History & Analysis
=======================
Track and analyze game history
"""

import json
from datetime import datetime


class GameHistory:
    """Track game history and statistics"""
    
    def __init__(self):
        self.games = []
        self.current_game = None
    
    def start_game(self, player_white='Human', player_black='AI'):
        """Start a new game"""
        self.current_game = {
            'start_time': datetime.now().isoformat(),
            'player_white': player_white,
            'player_black': player_black,
            'moves': [],
            'result': None,
            'captures': {'white': [], 'black': []}
        }
    
    def add_move(self, move_num, from_pos, to_pos, piece, captured=None, promotion=None):
        """Add a move to history"""
        if self.current_game:
            move = {
                'move_num': move_num,
                'from': from_pos,
                'to': to_pos,
                'piece': piece,
                'captured': captured,
                'promotion': promotion
            }
            self.current_game['moves'].append(move)
            
            if captured:
                color = 'white' if piece.color == 'black' else 'black'
                self.current_game['captures'][color].append(captured)
    
    def end_game(self, result, winner=None):
        """End current game"""
        if self.current_game:
            self.current_game['end_time'] = datetime.now().isoformat()
            self.current_game['result'] = result
            self.current_game['winner'] = winner
            
            # Calculate duration
            start = datetime.fromisoformat(self.current_game['start_time'])
            end = datetime.fromisoformat(self.current_game['end_time'])
            self.current_game['duration_seconds'] = (end - start).total_seconds()
            
            self.games.append(self.current_game)
            self.current_game = None
    
    def save_to_file(self, filename='chess_history.json'):
        """Save history to file"""
        data = {
            'games': self.games,
            'total_games': len(self.games)
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Game history saved to {filename}")
    
    def load_from_file(self, filename='chess_history.json'):
        """Load history from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.games = data.get('games', [])
                print(f"Loaded {len(self.games)} games")
        except FileNotFoundError:
            print("No saved history found")
    
    def get_statistics(self):
        """Get game statistics"""
        if not self.games:
            return "No games played yet"
        
        total = len(self.games)
        white_wins = sum(1 for g in self.games if g.get('winner') == 'white')
        black_wins = sum(1 for g in self.games if g.get('winner') == 'black')
        draws = total - white_wins - black_wins
        
        avg_duration = sum(g.get('duration_seconds', 0) for g in self.games) / total
        total_moves = sum(len(g.get('moves', [])) for g in self.games)
        
        stats = f"""
=== Game Statistics ===
Total Games: {total}
White Wins: {white_wins}
Black Wins: {black_wins}
Draws: {draws}
Average Duration: {avg_duration:.1f}s
Total Moves: {total_moves}
Average Moves/Game: {total_moves/total:.1f}
"""
        return stats


class GameAnalyzer:
    """Analyze game positions and moves"""
    
    def __init__(self, board):
        self.board = board
    
    def evaluate_position(self):
        """Evaluate current position"""
        score = 0
        material = self._count_material()
        position = self._evaluate_positions()
        activity = self._evaluate_activity()
        
        score = material + position + activity
        
        return {
            'total': score,
            'material': material,
            'position': position,
            'activity': activity,
            'assessment': self._get_assessment(score)
        }
    
    def _count_material(self):
        """Count material balance"""
        white_material = 0
        black_material = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece:
                    value = piece.get_value()
                    if piece.color == 'white':
                        white_material += value
                    else:
                        black_material += value
        
        return black_material - white_material
    
    def _evaluate_positions(self):
        """Evaluate piece positions"""
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece:
                    # Center control bonus
                    if 2 <= row <= 5 and 2 <= col <= 5:
                        bonus = 0.1 if piece.color == 'black' else -0.1
                        score += bonus
                    
                    # Development bonus
                    if piece.color == 'white' and row > 4:
                        score -= 0.05
                    elif piece.color == 'black' and row < 3:
                        score += 0.05
        
        return score
    
    def _evaluate_activity(self):
        """Evaluate piece activity"""
        from validator import MoveValidator
        validator = MoveValidator(self.board)
        
        white_moves = 0
        black_moves = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece:
                    moves = validator.get_valid_moves(row, col, piece.color)
                    if piece.color == 'white':
                        white_moves += len(moves)
                    else:
                        black_moves += len(moves)
        
        return (black_moves - white_moves) * 0.01
    
    def _get_assessment(self, score):
        """Get position assessment"""
        if abs(score) > 10:
            return "Decisive Advantage"
        elif abs(score) > 5:
            return "Significant Advantage"
        elif abs(score) > 2:
            return "Slight Advantage"
        else:
            return "Equal Position"
    
    def suggest_moves(self, color, max_suggestions=3):
        """Suggest best moves"""
        from validator import MoveValidator
        from ai import ChessAI
        
        validator = MoveValidator(self.board)
        ai = ChessAI(depth=2)
        
        # Get all valid moves
        all_moves = []
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    moves = validator.get_valid_moves(row, col, color)
                    for to_row, to_col in moves:
                        # Make move temporarily
                        captured = self.board.get_piece(to_row, to_col)
                        self.board.set_piece(to_row, to_col, piece)
                        self.board.remove_piece(row, col)
                        
                        # Evaluate
                        analyzer = GameAnalyzer(self.board)
                        eval_result = analyzer.evaluate_position()
                        
                        # Undo
                        self.board.set_piece(row, col, piece)
                        self.board.set_piece(to_row, to_col, captured)
                        
                        all_moves.append({
                            'from': (row, col),
                            'to': (to_row, to_col),
                            'score': eval_result['total']
                        })
        
        # Sort by score
        reverse = color == 'black'
        all_moves.sort(key=lambda x: x['score'], reverse=reverse)
        
        return all_moves[:max_suggestions]
