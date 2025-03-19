from flask import Flask, render_template, request, jsonify, session
from tetris_game import TetrisGame
import os
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Store active games
games = {}

@app.route('/')
def index():
    """Render the main game page"""
    return render_template('index.html')

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Start a new game and return the game ID"""
    game_id = str(uuid.uuid4())
    
    # Get game settings from request
    settings = request.json or {}
    speed_level = settings.get('speed_level', 1)
    scoring_system = settings.get('scoring_system', 'standard')
    
    games[game_id] = TetrisGame(
        speed_level=speed_level,
        scoring_system=scoring_system
    )
    return jsonify({'game_id': game_id, 'state': games[game_id].get_game_state()})

@app.route('/api/game_state/<game_id>', methods=['GET'])
def game_state(game_id):
    """Get the current game state"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify({'state': games[game_id].get_game_state()})

@app.route('/api/move/<game_id>', methods=['POST'])
def move(game_id):
    """Process a move in the game"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    action = request.json.get('action')
    
    if action == 'left':
        game.move_left()
    elif action == 'right':
        game.move_right()
    elif action == 'down':
        game.move_down()
    elif action == 'rotate':
        game.rotate()
    elif action == 'drop':
        game.drop()
    
    return jsonify({'state': game.get_game_state()})

@app.route('/telegram-web-app-init')
def telegram_web_app_init():
    """Special route for Telegram Web App initialization"""
    return render_template('telegram_init.html')

if __name__ == '__main__':
    app.run(debug=True)

