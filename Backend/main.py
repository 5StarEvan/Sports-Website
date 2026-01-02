"""
NBA AI Backend - Simplified version using only our AI system
No external NBA API dependencies required
"""

import numpy as np
from datetime import datetime

# Import AI predictions module
try:
    from nba_ai_system import get_top_scorers, get_top_assists, get_top_rebounders, get_breakout_players, get_player_prediction, initialize_nba_ai
    AI_AVAILABLE = True
except ImportError:
    print("AI predictions module not available. Install PyTorch dependencies to enable AI features.")
    AI_AVAILABLE = False

def read_favourite_players(filename='Backend/FavouritePlayers.txt'):
    """Read favorite players from file"""
    favourite_players = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                name = line.strip()
                if name:
                    favourite_players.append(name)
    except FileNotFoundError:
        print(f"{filename} not found.")
    return favourite_players

def get_ai_predictions():
    """Get AI predictions for top performers and breakout players"""
    if not AI_AVAILABLE:
        return {
            'error': 'AI predictions not available. Install PyTorch dependencies to enable AI features.',
            'top_scorers': [],
            'top_assists': [],
            'top_rebounders': [],
            'breakout_players': []
        }
    
    try:
        return {
            'top_scorers': get_top_scorers(10),
            'top_assists': get_top_assists(10),
            'top_rebounders': get_top_rebounders(10),
            'breakout_players': get_breakout_players(10)
        }
    except Exception as e:
        return {
            'error': f'Error getting AI predictions: {str(e)}',
            'top_scorers': [],
            'top_assists': [],
            'top_rebounders': [],
            'breakout_players': []
        }

def get_ai_player_prediction(player_name):
    """Get AI prediction for a specific player"""
    if not AI_AVAILABLE:
        return {'error': 'AI predictions not available. Install PyTorch dependencies.'}
    
    try:
        return get_player_prediction(player_name)
    except Exception as e:
        return {'error': f'Error getting prediction for {player_name}: {str(e)}'}

def initialize_ai_system():
    """Initialize the AI system"""
    if not AI_AVAILABLE:
        return {'error': 'AI predictions not available. Install PyTorch dependencies.'}
    
    try:
        success = initialize_nba_ai()
        if success:
            return {'status': 'success', 'message': 'AI system initialized successfully'}
        else:
            return {'error': 'Failed to initialize AI system'}
    except Exception as e:
        return {'error': f'Error initializing AI system: {str(e)}'}

def get_favorite_players_predictions():
    """Get predictions for favorite players"""
    if not AI_AVAILABLE:
        return {'error': 'AI predictions not available. Install PyTorch dependencies.'}
    
    try:
        favorite_players = read_favourite_players()
        predictions = []
        
        for player_name in favorite_players:
            prediction = get_player_prediction(player_name)
            if prediction and 'error' not in prediction:
                predictions.append(prediction)
        
        return {
            'favorite_players': predictions,
            'count': len(predictions)
        }
    except Exception as e:
        return {'error': f'Error getting favorite players predictions: {str(e)}'}

# Main execution
if __name__ == "__main__":
    print("🏀 NBA AI Backend - Simplified Version")
    print("=" * 50)
    
    # Initialize AI system
    print("Initializing AI system...")
    init_result = initialize_ai_system()
    if 'error' in init_result:
        print(f"❌ {init_result['error']}")
        exit(1)
    else:
        print("✅ AI system initialized successfully!")
    
    # Get AI predictions
    print("\n=== AI PREDICTIONS ===")
    ai_predictions = get_ai_predictions()
    
    if 'error' not in ai_predictions:
        print("\n🏆 Top 5 AI Predicted Scorers:")
        for i, scorer in enumerate(ai_predictions['top_scorers'][:5], 1):
            print(f"{i}. {scorer['PLAYER_NAME']} ({scorer['TEAM']}) - {scorer['PREDICTED_PPG']:.1f} PPG")
        
        print("\n🎯 Top 5 AI Predicted Assist Leaders:")
        for i, assist in enumerate(ai_predictions['top_assists'][:5], 1):
            print(f"{i}. {assist['PLAYER_NAME']} ({assist['TEAM']}) - {assist['PREDICTED_APG']:.1f} APG")
        
        print("\n🏀 Top 5 AI Predicted Rebounders:")
        for i, rebounder in enumerate(ai_predictions['top_rebounders'][:5], 1):
            print(f"{i}. {rebounder['PLAYER_NAME']} ({rebounder['TEAM']}) - {rebounder['PREDICTED_RPG']:.1f} RPG")
        
        print("\n🚀 Top 5 AI Predicted Breakout Players:")
        for i, breakout in enumerate(ai_predictions['breakout_players'][:5], 1):
            print(f"{i}. {breakout['PLAYER_NAME']} ({breakout['TEAM']}) - {breakout['TOTAL_IMPROVEMENT']:.1f}% improvement")
    else:
        print(f"❌ AI Error: {ai_predictions['error']}")
    
    # Get favorite players predictions
    print("\n=== FAVORITE PLAYERS PREDICTIONS ===")
    favorite_predictions = get_favorite_players_predictions()
    
    if 'error' not in favorite_predictions and favorite_predictions['count'] > 0:
        print(f"\nPredictions for {favorite_predictions['count']} favorite players:")
        for prediction in favorite_predictions['favorite_players']:
            print(f"\n{prediction['name']} ({prediction['team']}):")
            print(f"  Current: {prediction['current_stats']['ppg']:.1f} PPG, {prediction['current_stats']['apg']:.1f} APG, {prediction['current_stats']['rpg']:.1f} RPG")
            print(f"  Predicted: {prediction['predicted_stats']['ppg']:.1f} PPG, {prediction['predicted_stats']['apg']:.1f} APG, {prediction['predicted_stats']['rpg']:.1f} RPG")
            print(f"  Improvement: {prediction['improvements']['ppg']:+.1f}% PPG, {prediction['improvements']['apg']:+.1f}% APG, {prediction['improvements']['rpg']:+.1f}% RPG")
    else:
        print("No favorite players found or error occurred.")
    
    print("\n✅ NBA AI Backend completed successfully!")
    print("\n🎉 All predictions generated using our PyTorch AI system!")
