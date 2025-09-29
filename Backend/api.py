"""
Flask API for NBA AI Predictions
Serves AI predictions to the frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our AI functions
try:
    from main import get_ai_predictions, get_ai_player_prediction, initialize_ai_system, get_favorite_players_predictions
    AI_AVAILABLE = True
except ImportError as e:
    print(f"Error importing AI functions: {e}")
    AI_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize AI system on startup
@app.before_first_request
def initialize_ai():
    if AI_AVAILABLE:
        print("Initializing AI system...")
        result = initialize_ai_system()
        if 'error' in result:
            print(f"AI initialization error: {result['error']}")
        else:
            print("AI system initialized successfully!")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_available': AI_AVAILABLE,
        'message': 'NBA AI API is running'
    })

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    """Get all AI predictions"""
    if not AI_AVAILABLE:
        return jsonify({
            'error': 'AI predictions not available. Install PyTorch dependencies.',
            'ai_available': False
        }), 500
    
    try:
        predictions = get_ai_predictions()
        return jsonify({
            'success': True,
            'data': predictions,
            'ai_available': True
        })
    except Exception as e:
        return jsonify({
            'error': f'Error getting predictions: {str(e)}',
            'ai_available': True
        }), 500

@app.route('/api/predictions/top-scorers', methods=['GET'])
def get_top_scorers():
    """Get top predicted scorers"""
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    
    try:
        limit = request.args.get('limit', 10, type=int)
        predictions = get_ai_predictions()
        if 'error' in predictions:
            return jsonify({'error': predictions['error']}), 500
        
        return jsonify({
            'success': True,
            'data': predictions['top_scorers'][:limit]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictions/top-assists', methods=['GET'])
def get_top_assists():
    """Get top predicted assist leaders"""
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    
    try:
        limit = request.args.get('limit', 10, type=int)
        predictions = get_ai_predictions()
        if 'error' in predictions:
            return jsonify({'error': predictions['error']}), 500
        
        return jsonify({
            'success': True,
            'data': predictions['top_assists'][:limit]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictions/top-rebounders', methods=['GET'])
def get_top_rebounders():
    """Get top predicted rebounders"""
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    
    try:
        limit = request.args.get('limit', 10, type=int)
        predictions = get_ai_predictions()
        if 'error' in predictions:
            return jsonify({'error': predictions['error']}), 500
        
        return jsonify({
            'success': True,
            'data': predictions['top_rebounders'][:limit]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictions/breakout-players', methods=['GET'])
def get_breakout_players():
    """Get breakout players"""
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    
    try:
        limit = request.args.get('limit', 10, type=int)
        threshold = request.args.get('threshold', 5.0, type=float)
        predictions = get_ai_predictions()
        if 'error' in predictions:
            return jsonify({'error': predictions['error']}), 500
        
        # Filter breakout players by threshold
        breakout_players = predictions['breakout_players']
        filtered_players = [p for p in breakout_players if p.get('TOTAL_IMPROVEMENT', 0) > threshold]
        
        return jsonify({
            'success': True,
            'data': filtered_players[:limit]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/player/<player_name>', methods=['GET'])
def get_player_prediction(player_name):
    """Get prediction for a specific player"""
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    
    try:
        prediction = get_ai_player_prediction(player_name)
        if 'error' in prediction:
            return jsonify({'error': prediction['error']}), 404
        
        return jsonify({
            'success': True,
            'data': prediction
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """Get predictions for favorite players"""
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    
    try:
        favorites = get_favorite_players_predictions()
        if 'error' in favorites:
            return jsonify({'error': favorites['error']}), 500
        
        return jsonify({
            'success': True,
            'data': favorites
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/initialize', methods=['POST'])
def initialize_ai_endpoint():
    """Initialize the AI system"""
    if not AI_AVAILABLE:
        return jsonify({'error': 'AI not available'}), 500
    
    try:
        result = initialize_ai_system()
        if 'error' in result:
            return jsonify({'error': result['error']}), 500
        
        return jsonify({
            'success': True,
            'message': result.get('message', 'AI system initialized successfully')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🏀 Starting NBA AI API Server...")
    print("API Endpoints:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/predictions - All predictions")
    print("  GET  /api/predictions/top-scorers - Top scorers")
    print("  GET  /api/predictions/top-assists - Top assists")
    print("  GET  /api/predictions/top-rebounders - Top rebounders")
    print("  GET  /api/predictions/breakout-players - Breakout players")
    print("  GET  /api/player/<name> - Player prediction")
    print("  GET  /api/favorites - Favorite players")
    print("  POST /api/initialize - Initialize AI system")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
