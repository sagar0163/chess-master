"""
Chess Master Web Interface
==========================
Flask backend for web-based chess GUI
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from board import ChessBoard
from validator import MoveValidator
from ai import ChessAI
from display import ChessBoardDisplay
import json

app = Flask(__name__, template_folder='templates', static_folder='static')

# Game state storage (in-memory for simplicity)
games = {}
game_counter = 0


def load_config():
    """Load game configuration"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return {
            'difficulty_levels': {
                'beginner': {'depth': 2, 'skill_level': 2, 'randomness': 0.3},
                'intermediate': {'depth': 3, 'skill_level': 5, 'randomness': 0.15},
                'advanced': {'depth': 4, 'skill_level': 8, 'randomness': 0.08},
                'grandmaster': {'depth': 6, 'skill_level': 10, 'randomness': 0.02}
            },
            'default_difficulty': 'grandmaster'
        }


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Start a new game"""
    global game_counter
    
    data = request.get_json() or {}
    difficulty = data.get('difficulty', 'grandmaster')
    player_color = data.get('player_color', 'white')
    
    config = load_config()
    diff_config = config.get('difficulty_levels', {}).get(difficulty, {})
    
    game_id = game_counter
    game_counter += 1
    
    game_state = {
        'id': game_id,
        'board': ChessBoard(),
        'validator': MoveValidator(ChessBoard()),
        'display': ChessBoardDisplay(),
        'difficulty': difficulty,
        'depth': diff_config.get('depth', 6),
        'ai': ChessAI(depth=diff_config.get('depth', 6), difficulty=difficulty),
        'player_color': player_color,
        'game_over': False,
        'winner': None,
        'move_history': [],
        'current_turn': 'white'
    }
    
    # Re-create validator with correct board
    game_state['validator'] = MoveValidator(game_state['board'])
    
    games[game_id] = game_state
    
    return jsonify({
        'game_id': game_id,
        'board': game_state['board'].get_board_state(),
        'current_turn': game_state['current_turn'],
        'difficulty': difficulty,
        'player_color': player_color,
        'fen': game_state['board'].to_fen()
    })


@app.route('/api/get_board/<int:game_id>', methods=['GET'])
def get_board(game_id):
    """Get current board state"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    return jsonify({
        'board': game['board'].get_board_state(),
        'current_turn': game['current_turn'],
        'game_over': game['game_over'],
        'winner': game['winner'],
        'move_history': game['move_history'],
        'fen': game['board'].to_fen()
    })


@app.route('/api/move', methods=['POST'])
def make_move():
    """Make a move"""
    data = request.get_json()
    game_id = data.get('game_id')
    from_pos = data.get('from')  # [row, col]
    to_pos = data.get('to')      # [row, col]
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    if game['game_over']:
        return jsonify({'error': 'Game is over'}), 400
    
    # Check if it's player's turn
    if game['current_turn'] != game['player_color']:
        return jsonify({'error': 'Not your turn'}), 400
    
    # Validate and make move
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    
    valid, reason = game['validator'].is_valid_move(
        from_row, from_col, to_row, to_col,
        game['current_turn']
    )
    
    if not valid:
        return jsonify({'error': reason}), 400
    
    # Make the move
    game['board'].make_move(from_row, from_col, to_row, to_col)
    game['move_history'].append({
        'from': from_pos,
        'to': to_pos,
        'color': game['current_turn']
    })
    
    # Switch turn
    game['current_turn'] = 'black' if game['current_turn'] == 'white' else 'white'
    
    # Check for game over
    if _check_game_over(game):
        return jsonify({
            'board': game['board'].get_board_state(),
            'current_turn': game['current_turn'],
            'game_over': game['game_over'],
            'winner': game['winner'],
            'fen': game['board'].to_fen()
        })
    
    # AI move if it's AI's turn
    if game['current_turn'] != game['player_color'] and not game['game_over']:
        return jsonify({
            'board': game['board'].get_board_state(),
            'current_turn': game['current_turn'],
            'game_over': game['game_over'],
            'waiting_for_ai': True,
            'fen': game['board'].to_fen()
        })
    
    return jsonify({
        'board': game['board'].get_board_state(),
        'current_turn': game['current_turn'],
        'game_over': game['game_over'],
        'fen': game['board'].to_fen()
    })


@app.route('/api/ai_move/<int:game_id>', methods=['POST'])
def ai_move(game_id):
    """Make AI move"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    if game['game_over']:
        return jsonify({'error': 'Game is over'}), 400
    
    if game['current_turn'] == game['player_color']:
        return jsonify({'error': 'Not AI turn'}), 400
    
    # Get AI move
    move = game['ai'].get_best_move(game['board'], game['current_turn'])
    
    if move:
        from_pos, to_pos = move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        game['board'].make_move(from_row, from_col, to_row, to_col)
        game['move_history'].append({
            'from': [from_row, from_col],
            'to': [to_row, to_col],
            'color': game['current_turn']
        })
    
    # Switch turn
    game['current_turn'] = 'black' if game['current_turn'] == 'white' else 'white'
    
    # Check for game over
    _check_game_over(game)
    
    return jsonify({
        'board': game['board'].get_board_state(),
        'current_turn': game['current_turn'],
        'game_over': game['game_over'],
        'winner': game['winner'],
        'ai_move': move,
        'fen': game['board'].to_fen()
    })


@app.route('/api/difficulties', methods=['GET'])
def get_difficulties():
    """Get available difficulty levels"""
    config = load_config()
    return jsonify(config.get('difficulty_levels', {}))


def _check_game_over(game):
    """Check if game is over"""
    color = game['current_turn']
    has_moves = False
    
    for row in range(8):
        for col in range(8):
            piece = game['board'].get_piece(row, col)
            if piece and piece.color == color:
                moves = game['validator'].get_valid_moves(row, col, color)
                if moves:
                    has_moves = True
                    break
    
    if not has_moves:
        game['game_over'] = True
        if game['board'].is_in_check(color):
            game['winner'] = 'black' if color == 'white' else 'white'
        else:
            game['winner'] = 'draw'
        return True
    
    return False


if __name__ == '__main__':
    print("� Chess Master Web Interface")
    print("=" * 40)
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
