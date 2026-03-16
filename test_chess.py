"""Unit tests for Chess game"""

import pytest
from chess import ChessBoard, ChessAI


class TestChessBoard:
    def test_board_initialization(self):
        board = ChessBoard()
        assert board is not None
        # Check initial piece placement
        assert board.get_piece(0, 0) == 'R'  # White rook
        assert board.get_piece(7, 4) == 'k'  # Black king
    
    def test_valid_moves(self):
        board = ChessBoard()
        moves = board.get_valid_moves(1, 0)  # White knight
        assert len(moves) > 0
    
    def test_make_move(self):
        board = ChessBoard()
        initial_piece = board.get_piece(1, 0)
        board.make_move((1, 0), (2, 0))
        assert board.get_piece(2, 0) == initial_piece
    
    def test_check_detection(self):
        board = ChessBoard()
        # Set up a simple check
        board.set_piece(7, 4, 'K')  # Black king
        board.set_piece(6, 3, 'Q')  # White queen
        assert board.is_in_check('K') == True


class TestChessAI:
    def test_ai_initialization(self):
        ai = ChessAI(difficulty=3)
        assert ai.depth == 3
    
    def test_get_best_move(self):
        ai = ChessAI(difficulty=1)
        board = ChessBoard()
        move = ai.get_best_move(board)
        assert move is not None
    
    def test_evaluate_board(self):
        ai = ChessAI()
        board = ChessBoard()
        score = ai.evaluate_board(board)
        # Should return a numeric score
        assert isinstance(score, (int, float))
