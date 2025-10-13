"""
Flask API for NBA AI Predictions
Serves AI predictions to the frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add current directory to path for importing AI functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import AI functions from main.py
try:
    from main import (
        initialize_nba_ai,
        get_top_scorers,
        get_top_assists,
        get_top_rebounders,
        get_breakout_players,
        get_player_prediction
    )
    AI_AVAILABLE = True
except ImportError as e:
    print(f"Error importing AI functions: {e}")
    AI_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize AI system at startup
if AI_AVAILABLE:
    print("Initializing NBA AI system...")
    try:
        if not initialize_nba_ai():
            print("❌ AI system initialization failed")
        else:
            print("✅ AI system initialized successfully!")
    except Exception as e:
        print(f"AI initialization error: {e}")


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'ai_available': AI_AVAILABLE})


@app.route('/api/predictions', methods=['GET'])
def all_predictions():
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    try:
        predictions = get_top_scorers(limit=10)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predictions/top-assists', methods=['GET'])
def top_assists():
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    try:
        predictions = get_top_assists(limit=10)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predictions/top-rebounders', methods=['GET'])
def top_rebounders():
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    try:
        predictions = get_top_rebounders(limit=10)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predictions/breakout-players', methods=['GET'])
def breakout_players():
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    try:
        threshold = request.args.get('threshold', 5.0, type=float)
        predictions = get_breakout_players(limit=10, threshold=threshold)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/player/<player_name>', methods=['GET'])
def player_prediction_endpoint(player_name):
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    try:
        prediction = get_player_prediction(player_name)
        if prediction is None:
            return jsonify({'error': 'Player not found'}), 404
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🏀 Starting NBA AI API Server...")
    print("API Endpoints:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/predictions - Top scorers")
    print("  GET  /api/predictions/top-assists - Top assists")
    print("  GET  /api/predictions/top-rebounders - Top rebounders")
    print("  GET  /api/predictions/breakout-players - Breakout players")
    print("  GET  /api/player/<name> - Player prediction")

    app.run(debug=True, host='0.0.0.0', port=5000)
