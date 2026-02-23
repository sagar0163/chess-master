"""
Chess AI Engine
===============
Minimax-based AI opponent with difficulty levels
"""

import random
from pieces import King, Queen, Rook, Bishop, Knight, Pawn
import json
import os


class ChessAI:
    """AI opponent using minimax algorithm"""
    
    def __init__(self, depth=3, difficulty='intermediate'):
        self.depth = depth
        self.difficulty = difficulty
        self.nodes_evaluated = 0
        self._load_difficulty_config()
    
    def _load_difficulty_config(self):
        """Load difficulty configuration"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                diff_config = config.get('difficulty_levels', {}).get(self.difficulty, {})
                self.skill_level = diff_config.get('skill_level', 5)
                self.randomness = diff_config.get('randomness', 0.1)
        except:
            self.skill_level = 5
            self.randomness = 0.1
    
    def get_best_move(self, board, color):
        """Get best move for AI"""
        self.nodes_evaluated = 0
        
        # Get all valid moves
        from validator import MoveValidator
        validator = MoveValidator(board)
        
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == color:
                    moves = validator.get_valid_moves(row, col, color)
                    for to_row, to_col in moves:
                        all_moves.append(((row, col), (to_row, to_col)))
        
        if not all_moves:
            return None
        
        # For Grandmaster: use full minimax with best move selection
        # Apply randomness based on difficulty (lower = more randomness)
        if self.randomness > 0 and random.random() < self.randomness:
            # Introduce occasional suboptimal moves for lower difficulties
            sorted_moves = self._get_sorted_moves(board, all_moves, color)
            # Pick from top 3-5 moves randomly
            top_n = min(len(sorted_moves), max(3, int(5 * (1 - self.skill_level/10))))
            return random.choice(sorted_moves[:top_n])
        
        # Minimax with alpha-beta pruning
        best_move = None
        best_score = float('-inf') if color == 'black' else float('inf')
        
        alpha = float('-inf')
        beta = float('inf')
        
        for move in all_moves:
            # Make move
            from_row, from_col = move[0]
            to_row, to_col = move[1]
            
            piece = board.get_piece(from_row, from_col)
            captured = board.get_piece(to_row, to_col)
            
            board.set_piece(to_row, to_col, piece)
            board.remove_piece(from_row, from_col)
            
            # Evaluate
            if color == 'black':
                score = self._minimax(board, self.depth - 1, alpha, beta, 'white')
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, score)
            else:
                score = self._minimax(board, self.depth - 1, alpha, beta, 'black')
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)
            
            # Undo move
            board.set_piece(from_row, from_col, piece)
            board.set_piece(to_row, to_col, captured)
        
        return best_move
    
    def _get_sorted_moves(self, board, moves, color):
        """Get moves sorted by evaluation for smarter random selection"""
        move_scores = []
        from validator import MoveValidator
        validator = MoveValidator(board)
        
        for move in moves:
            from_row, from_col = move[0]
            to_row, to_col = move[1]
            
            piece = board.get_piece(from_row, from_col)
            captured = board.get_piece(to_row, to_col)
            
            board.set_piece(to_row, to_col, piece)
            board.remove_piece(from_row, from_col)
            
            score = self._evaluate_board(board)
            
            board.set_piece(from_row, from_col, piece)
            board.set_piece(to_row, to_col, captured)
            
            # For black, higher score is better; for white, lower is better
            adjusted_score = score if color == 'black' else -score
            move_scores.append((move, adjusted_score))
        
        move_scores.sort(key=lambda x: x[1], reverse=(color == 'black'))
        return [m[0] for m in move_scores]
    
    def _minimax(self, board, depth, alpha, beta, color):
        """Minimax algorithm with alpha-beta pruning"""
        self.nodes_evaluated += 1
        
        # Terminal conditions
        if depth == 0:
            return self._evaluate_board(board)
        
        # Get all valid moves
        from validator import MoveValidator
        validator = MoveValidator(board)
        
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == color:
                    moves = validator.get_valid_moves(row, col, color)
                    for to_row, to_col in moves:
                        all_moves.append(((row, col), (to_row, to_col)))
        
        if not all_moves:
            # Checkmate or stalemate
            if board.is_in_check(color):
                return 10000 if color == 'black' else -10000
            return 0
        
        if color == 'black':
            # Maximizing
            max_score = float('-inf')
            for move in all_moves:
                from_row, from_col = move[0]
                to_row, to_col = move[1]
                
                piece = board.get_piece(from_row, from_col)
                captured = board.get_piece(to_row, to_col)
                
                board.set_piece(to_row, to_col, piece)
                board.remove_piece(from_row, from_col)
                
                score = self._minimax(board, depth - 1, alpha, beta, 'white')
                
                board.set_piece(from_row, from_col, piece)
                board.set_piece(to_row, to_col, captured)
                
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                
                if beta <= alpha:
                    break
            
            return max_score
        else:
            # Minimizing
            min_score = float('inf')
            for move in all_moves:
                from_row, from_col = move[0]
                to_row, to_col = move[1]
                
                piece = board.get_piece(from_row, from_col)
                captured = board.get_piece(to_row, to_col)
                
                board.set_piece(to_row, to_col, piece)
                board.remove_piece(from_row, from_col)
                
                score = self._minimax(board, depth - 1, alpha, beta, 'black')
                
                board.set_piece(from_row, from_col, piece)
                board.set_piece(to_row, to_col, captured)
                
                min_score = min(min_score, score)
                beta = min(beta, score)
                
                if beta <= alpha:
                    break
            
            return min_score
    
    def _evaluate_board(self, board):
        """Evaluate board position"""
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    # Material
                    value = piece.get_value()
                    
                    # Position bonus
                    bonus = self._get_position_bonus(piece, row, col)
                    
                    if piece.color == 'black':
                        score += value + bonus
                    else:
                        score -= value + bonus
        
        return score
    
    def _get_position_bonus(self, piece, row, col):
        """Get position-based bonus"""
        # Pawn position table (simplified)
        pawn_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5, -10,  0,  0, -10, -5,  5],
            [5, 10, 10, -20, -20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        
        if isinstance(piece, Pawn):
            return pawn_table[row][col]
        
        # Knight position table
        knight_table = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20,  0,  0,  0,  0, -20, -40],
            [-30,  0, 10, 15, 15, 10,  0, -30],
            [-30,  5, 15, 20, 20, 15,  5, -30],
            [-30,  0, 15, 20, 20, 15,  0, -30],
            [-30,  5, 10, 15, 15, 10,  5, -30],
            [-40, -20,  0,  5,  5,  0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ]
        
        if isinstance(piece, Knight):
            return knight_table[row][col]
        
        return 0
