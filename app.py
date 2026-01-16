from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pickle
import json
import os
import secrets
import subprocess
import sys
import signal
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from functools import wraps
# from db import init_db, create_user_from_json, authenticate_user_from_json, get_user_by_id

try:
    from nba_ai_system import get_top_scorers, get_top_assists, get_top_rebounders, get_breakout_players, get_player_prediction, initialize_nba_ai
    AI_AVAILABLE = True
except ImportError as e:
    print(f"AI predictions module not available: {e}")
    AI_AVAILABLE = False

app = Flask(__name__)

AO = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:5173').split(',')
CORS(app, resources={
    r"/api/*": {
        "origins": AO,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SECRET_KEY'] = SECRET_KEY

TOKEN_EXPIRY_HOURS = 24
active_tokens = {}

# mysql = None
# try:
#     mysql = init_db(app)
#     print("Database connection configured successfully")
# except Exception as e:
#     print(f"Database initialization error: {e}")
#     mysql = None
mysql = None

nba_data = None

def create_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expiry = datetime.now() + timedelta(hours=TOKEN_EXPIRY_HOURS)
    active_tokens[token] = {
        'user_id': user_id,
        'expiry': expiry
    }
    return token

def validate_token(token: str) -> Optional[int]:
    if token not in active_tokens:
        return None
    
    token_data = active_tokens[token]
    if datetime.now() > token_data['expiry']:
        del active_tokens[token]
        return None
    
    return token_data['user_id']

def invalidate_token(token: str):
    if token in active_tokens:
        del active_tokens[token]

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'message': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = validate_token(token)
        
        if not user_id:
            return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
        
        request.user_id = user_id
        return f(*args, **kwargs)
    
    return decorated_function

def sanitize_string(value: str, max_length: int = 100) -> str:
    if not isinstance(value, str):
        return ""
    return value[:max_length].strip()

def validate_pagination(page: any, limit: any) -> tuple:
    try:
        page = max(int(page), 1)
    except (ValueError, TypeError):
        page = 1
    
    try:
        limit = min(max(int(limit), 1), 100)
    except (ValueError, TypeError):
        limit = 20
    
    return page, limit

def load_nba_data():
    global nba_data
    try:
        with open('nba_2024_25_data.pkl', 'rb') as f:
            nba_data = pickle.load(f)
        print(f"Loaded {len(nba_data)} NBA players from pickle file")
        return True
    except FileNotFoundError:
        print("NBA data file 'nba_2024_25_data.pkl' not found.")
        return False
    except Exception as e:
        print(f"Error loading NBA data: {e}")
        return False

def get_player_stats_summary(player_data):
    ppg_current = player_data.get('PPG_LAST', player_data.get('ppg_last', 0))
    ppg_prev = player_data.get('PPG_PREV', player_data.get('ppg_prev', ppg_current))
    ppg_trend = round(ppg_current - ppg_prev, 2) if ppg_prev else 0
    
    apg_current = player_data.get('APG_LAST', player_data.get('apg_last', 0))
    apg_prev = player_data.get('APG_PREV', player_data.get('apg_prev', apg_current))
    apg_trend = round(apg_current - apg_prev, 2) if apg_prev else 0
    
    rpg_current = player_data.get('RPG_LAST', player_data.get('rpg_last', 0))
    rpg_prev = player_data.get('RPG_PREV', player_data.get('rpg_prev', rpg_current))
    rpg_trend = round(rpg_current - rpg_prev, 2) if rpg_prev else 0
    
    ppg_std = player_data.get('PPG_STD', player_data.get('ppg_std', 5))
    consistency_score = round(max(0, 1 - (ppg_std / 20)), 2)
    
    return {
        'id': player_data.get('PLAYER_ID', player_data.get('player_id', hash(player_data.get('PLAYER_NAME', '')))),
        'name': player_data.get('PLAYER_NAME', player_data.get('player_name', 'Unknown')),
        'team': player_data.get('TEAM', player_data.get('team', 'UNK')),
        'position': player_data.get('POSITION', player_data.get('position', 'UNK')),
        'age': player_data.get('AGE', player_data.get('age', 0)),
        'height': player_data.get('HEIGHT', player_data.get('height', 0)),
        'weight': player_data.get('WEIGHT', player_data.get('weight', 0)),
        'stats': {
            'ppg_last': round(ppg_current, 1),
            'apg_last': round(apg_current, 1),
            'rpg_last': round(rpg_current, 1),
            'spg_last': round(player_data.get('SPG_LAST', player_data.get('spg_last', 0)), 1),
            'bpg_last': round(player_data.get('BPG_LAST', player_data.get('bpg_last', 0)), 1),
            'fg_pct_last': round(player_data.get('FG_PCT_LAST', player_data.get('fg_pct_last', 0)) * 100, 1),
            'fg3_pct_last': round(player_data.get('FG3_PCT_LAST', player_data.get('fg3_pct_last', 0)) * 100, 1),
            'ft_pct_last': round(player_data.get('FT_PCT_LAST', player_data.get('ft_pct_last', 0)) * 100, 1),
            'games_played': player_data.get('GAMES_PLAYED_LAST', player_data.get('games_played_last', 0))
        },
        'trends': {
            'ppg_trend': round(player_data.get('PPGTREND', ppg_trend), 2),
            'apg_trend': round(player_data.get('APGTREND', apg_trend), 2),
            'rpg_trend': round(player_data.get('RPGTREND', rpg_trend), 2),
            'consistency_score': round(player_data.get('CONSISTENCYSCORE', consistency_score), 2)
        }
    }

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# @app.route('/api/auth/signup', methods=['POST'])
# @limiter.limit("5 per hour")
# def signup():
#     if not mysql:
#         return jsonify({
#             'success': False,
#             'message': 'Database connection not available'
#         }), 500
    
#     try:
#         success, user, message = create_user_from_json(mysql)
        
#         if success:
#             token = create_token(user['id'])
#             return jsonify({
#                 'success': True,
#                 'user': user,
#                 'token': token,
#                 'message': message
#             }), 201
#         else:
#             return jsonify({
#                 'success': False,
#                 'message': message
#             }), 400
#     except Exception as e:
#         print(f"Signup error: {e}")
#         return jsonify({
#             'success': False,
#             'message': 'An error occurred while creating your account'
#         }), 500

@app.route('/api/auth/signup', methods=['POST'])
@limiter.limit("5 per hour")
def signup():
    return jsonify({
        'success': False,
        'message': 'Database connection not available'
    }), 503

# @app.route('/api/auth/login', methods=['POST'])
# @limiter.limit("10 per hour")
# def login():
#     if not mysql:
#         return jsonify({
#             'success': False,
#             'message': 'Database connection not available'
#         }), 500
    
#     try:
#         success, user, message = authenticate_user_from_json(mysql)
        
#         if success:
#             token = create_token(user['id'])
#             return jsonify({
#                 'success': True,
#                 'user': user,
#                 'token': token,
#                 'message': message
#             }), 200
#         else:
#             return jsonify({
#                 'success': False,
#                 'message': message
#             }), 401
#     except Exception as e:
#         print(f"Login error: {e}")
#         return jsonify({
#             'success': False,
#             'message': 'An error occurred while logging in'
#         }), 500

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("10 per hour")
def login():
    return jsonify({
        'success': False,
        'message': 'Database connection not available'
    }), 503

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():

    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        invalidate_token(token)
    
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200

# @app.route('/api/auth/verify', methods=['GET'])
# def verify():
#     if not mysql:
#         return jsonify({
#             'authenticated': False,
#             'message': 'Database connection not available'
#         }), 500
    
#     try:
#         auth_header = request.headers.get('Authorization')
#         if not auth_header or not auth_header.startswith('Bearer '):
#             return jsonify({
#                 'authenticated': False,
#                 'message': 'No token provided'
#             }), 401
        
#         token = auth_header.split(' ')[1]
#         user_id = validate_token(token)
        
#         if not user_id:
#             return jsonify({
#                 'authenticated': False,
#                 'message': 'Invalid or expired token'
#             }), 401
        
#         user = get_user_by_id(mysql, user_id)
#         if user:
#             return jsonify({
#                 'authenticated': True,
#                 'user': user
#             }), 200
        
#         return jsonify({
#             'authenticated': False,
#             'message': 'User not found'
#         }), 401
#     except Exception as e:
#         print(f"Verify error: {e}")
#         return jsonify({
#             'authenticated': False,
#             'message': 'Error verifying token'
#         }), 500
@app.route('/api/auth/verify', methods=['GET'])
def verify():
    return jsonify({
        'authenticated': False,
        'message': 'Database connection not available'
    }), 503

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'NBA Sports Website API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'all_players': '/api/players',
            'player_by_id': '/api/players/<id>',
            'search_player': '/api/players/search/<name>',
            'teams': '/api/teams',
            'positions': '/api/positions',
            'ai_predictions': '/api/ai-predictions',
            'player_prediction': '/api/player-prediction/<name>',
            'stat_leaders': '/api/stats/leaders'
        },
        'players_loaded': len(nba_data) if nba_data else 0,
        'ai_available': AI_AVAILABLE
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'NBA API server is running',
        'ai_available': AI_AVAILABLE,
        'players_loaded': len(nba_data) if nba_data else 0,
        'database_connected': False  # mysql is not None
    })

@app.route('/api/players', methods=['GET'])
@limiter.limit("100 per hour")
def get_all_players():
    if not nba_data:
        return jsonify({'error': 'NBA data not loaded'}), 500
    
    page = request.args.get('page', 1)
    limit = request.args.get('limit', 20)
    page, limit = validate_pagination(page, limit)
    
    search = sanitize_string(request.args.get('search', ''), 50).lower()
    team = sanitize_string(request.args.get('team', ''), 10).upper()
    position = sanitize_string(request.args.get('position', ''), 10).upper()
    
    filtered_players = nba_data
    
    if search:
        filtered_players = [p for p in filtered_players if search in p['PLAYER_NAME'].lower()]
    
    if team:
        filtered_players = [p for p in filtered_players if p['TEAM'] == team]
    
    if position:
        filtered_players = [p for p in filtered_players if p['POSITION'] == position]
    
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    page_players = filtered_players[start_idx:end_idx]
    
    players_summary = [get_player_stats_summary(player) for player in page_players]
    
    return jsonify({
        'players': players_summary,
        'pagination': {
            'page': page,
            'limit': limit,
            'total': len(filtered_players),
            'total_pages': (len(filtered_players) + limit - 1) // limit
        },
        'filters': {
            'search': search,
            'team': team,
            'position': position
        }
    })

@app.route('/api/players/<int:player_id>', methods=['GET'])
@limiter.limit("200 per hour")
def get_player_by_id(player_id):
    if not nba_data:
        return jsonify({'error': 'NBA data not loaded'}), 500
    
    if player_id < 0 or player_id > 9999999:
        return jsonify({'error': 'Invalid player ID'}), 400
    
    player = next((p for p in nba_data if p['PLAYER_ID'] == player_id), None)
    if not player:
        return jsonify({'error': 'Player not found'}), 404
    
    return jsonify(get_player_stats_summary(player))

@app.route('/api/players/search/<string:player_name>', methods=['GET'])
@limiter.limit("100 per hour")
def search_player(player_name):
    if not nba_data:
        return jsonify({'error': 'NBA data not loaded'}), 500
    
    player_name_clean = sanitize_string(player_name, 50).lower()
    if not player_name_clean:
        return jsonify({'error': 'Invalid player name'}), 400
    
    players = [p for p in nba_data if player_name_clean in p['PLAYER_NAME'].lower()]
    
    if not players:
        return jsonify({'error': 'No players found'}), 404
    
    players_summary = [get_player_stats_summary(player) for player in players[:50]]
    return jsonify({'players': players_summary})

@app.route('/api/teams', methods=['GET'])
@limiter.limit("100 per hour")
def get_teams():
    if not nba_data:
        return jsonify({'error': 'NBA data not loaded'}), 500
    
    teams = list(set(player['TEAM'] for player in nba_data))
    teams.sort()
    return jsonify({'teams': teams})

@app.route('/api/positions', methods=['GET'])
@limiter.limit("100 per hour")
def get_positions():
    if not nba_data:
        return jsonify({'error': 'NBA data not loaded'}), 500
    
    positions = list(set(player['POSITION'] for player in nba_data))
    positions.sort()
    return jsonify({'positions': positions})

@app.route('/api/ai-predictions', methods=['GET'])
@limiter.limit("20 per hour")
def get_ai_predictions():
    if not AI_AVAILABLE:
        return jsonify({
            'error': 'AI predictions not available',
            'ai_available': False
        }), 503
    
    try:
        initialize_nba_ai()
        
        predictions = {
            'top_scorers': get_top_scorers(10),
            'top_assists': get_top_assists(10),
            'top_rebounders': get_top_rebounders(10),
            'breakout_players': get_breakout_players(10)
        }
        
        if nba_data:
            for category in ['top_scorers', 'top_assists', 'top_rebounders']:
                for player in predictions[category]:
                    player_name = player['PLAYER_NAME']
                    matching_player = next((p for p in nba_data if p['PLAYER_NAME'] == player_name), None)
                    if matching_player:
                        player['PPG_LAST'] = matching_player.get('PPG_LAST', 0)
                        player['APG_LAST'] = matching_player.get('APG_LAST', 0)
                        player['RPG_LAST'] = matching_player.get('RPG_LAST', 0)
        
        return jsonify({
            'predictions': predictions,
            'ai_available': True
        })
    except Exception as e:
        print(f"AI prediction error: {e}")
        return jsonify({
            'error': 'Error generating predictions',
            'ai_available': True
        }), 500

@app.route('/api/player-prediction/<string:player_name>', methods=['GET'])
@limiter.limit("30 per hour")
def get_player_prediction_api(player_name):
    if not AI_AVAILABLE:
        return jsonify({
            'error': 'AI predictions not available',
            'ai_available': False
        }), 503
    
    player_name_clean = sanitize_string(player_name, 50)
    if not player_name_clean:
        return jsonify({'error': 'Invalid player name'}), 400
    
    try:
        prediction = get_player_prediction(player_name_clean)
        return jsonify({
            'prediction': prediction,
            'ai_available': True
        })
    except Exception as e:
        print(f"Player prediction error: {e}")
        return jsonify({
            'error': 'Error generating prediction',
            'ai_available': True
        }), 500

@app.route('/api/stats/leaders', methods=['GET'])
@limiter.limit("100 per hour")
def get_stat_leaders():
    if not nba_data:
        return jsonify({'error': 'NBA data not loaded'}), 500
    
    ppg_leaders = sorted(nba_data, key=lambda x: x['PPG_LAST'], reverse=True)[:10]
    apg_leaders = sorted(nba_data, key=lambda x: x['APG_LAST'], reverse=True)[:10]
    rpg_leaders = sorted(nba_data, key=lambda x: x['RPG_LAST'], reverse=True)[:10]
    
    def format_leaders(leaders, stat_key, stat_name):
        return [{
            'name': player['PLAYER_NAME'],
            'team': player['TEAM'],
            'value': round(player[stat_key], 1),
            'stat_name': stat_name
        } for player in leaders]
    
    return jsonify({
        'ppg_leaders': format_leaders(ppg_leaders, 'PPG_LAST', 'Points Per Game'),
        'apg_leaders': format_leaders(apg_leaders, 'APG_LAST', 'Assists Per Game'),
        'rpg_leaders': format_leaders(rpg_leaders, 'RPG_LAST', 'Rebounds Per Game')
    })

if __name__ == '__main__':
    frontend_process = None
    
    def cleanup_processes():
        if frontend_process:
            try:
                print("\nStopping frontend server...")
                frontend_process.terminate()
                frontend_process.wait(timeout=5)
                print(" Frontend server stopped")
            except Exception as e:
                print(f"Error stopping frontend: {e}")
                try:
                    frontend_process.kill()
                except:
                    pass
    
    def signal_handler(sig, frame):
        cleanup_processes()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        print("🌐 Starting frontend development server...")
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(backend_dir)
        
        package_json = os.path.join(project_root, 'package.json')
        if os.path.exists(package_json):
            try:
                frontend_process = subprocess.Popen(
                    ['npm', 'run', 'dev'],
                    cwd=project_root,
                    shell=(sys.platform == 'win32')
                )
                print("Frontend server starting...")
                print(f"   Frontend: http://localhost:5173")
                time.sleep(3)
            except Exception as e:
                print(f"Frontend startup failed: {e}")
        
        print("\n🔄 Loading NBA data...")
        if load_nba_data():
            print(f"NBA data loaded - {len(nba_data)} players")
            for i, player in enumerate(nba_data[:5]):
                print(f"  {i+1}. {player['PLAYER_NAME']} ({player['TEAM']}) - {player['PPG_LAST']:.1f} PPG")
        else:
            nba_data = [
                {
                    'PLAYER_ID': 1,
                    'PLAYER_NAME': 'LeBron James',
                    'TEAM': 'LAL',
                    'POSITION': 'SF',
                    'AGE': 39,
                    'HEIGHT': 80,
                    'WEIGHT': 250,
                    'PPG_LAST': 25.0,
                    'APG_LAST': 7.8,
                    'RPG_LAST': 7.3,
                    'SPG_LAST': 1.3,
                    'BPG_LAST': 0.5,
                    'FG_PCT_LAST': 0.525,
                    'FG3_PCT_LAST': 0.410,
                    'FT_PCT_LAST': 0.730,
                    'GAMES_PLAYED_LAST': 71,
                    'PPG_TREND': 0.5,
                    'APG_TREND': 0.2,
                    'RPG_TREND': 0.1,
                    'CONSISTENCY_SCORE': 0.85
                },
                {
                    'PLAYER_ID': 2,
                    'PLAYER_NAME': 'Stephen Curry',
                    'TEAM': 'GSW',
                    'POSITION': 'PG',
                    'AGE': 35,
                    'HEIGHT': 75,
                    'WEIGHT': 190,
                    'PPG_LAST': 26.4,
                    'APG_LAST': 4.5,
                    'RPG_LAST': 4.5,
                    'SPG_LAST': 0.9,
                    'BPG_LAST': 0.4,
                    'FG_PCT_LAST': 0.450,
                    'FG3_PCT_LAST': 0.427,
                    'FT_PCT_LAST': 0.923,
                    'GAMES_PLAYED_LAST': 74,
                    'PPG_TREND': 1.2,
                    'APG_TREND': -0.1,
                    'RPG_TREND': 0.3,
                    'CONSISTENCY_SCORE': 0.92
                }
            ]
            print(f"Using sample data - {len(nba_data)} players")
        
        if AI_AVAILABLE:
            try:
                print("Initializing AI system...")
                initialize_nba_ai()
                print("AI system initialized")
            except Exception as e:
                print(f"AI initialization failed: {e}")
        
        print("\n" + "="*50)
        print("Starting NBA API server...")
        print("Backend: http://localhost:5000")
        print("Frontend: http://localhost:5173")
        print("Health: http://localhost:5000/api/health")
        print("="*50)
        print("Press Ctrl+C to stop")
        print("="*50 + "\n")
        
        app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
        
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        cleanup_processes()
        print("Server stopped")
    except Exception as e:
        print(f"Server error: {e}")
        cleanup_processes()