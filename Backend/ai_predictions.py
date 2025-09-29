"""
AI Predictions Module - Integration with existing backend
Provides easy-to-use functions for the web frontend
"""

import os
import json
from typing import Dict, List, Optional
from nba_ai_predictor import NBAAIPredictor

class AIPredictions:
    """Simple interface for AI predictions to be used by the web backend"""
    
    def __init__(self):
        self.predictor = NBAAIPredictor()
        self._ensure_model_loaded()
    
    def _ensure_model_loaded(self):
        """Ensure the model is loaded and ready for predictions"""
        if not self.predictor.model_trained:
            # Try to load existing model
            if not self.predictor.analyzer.load_model():
                print("Warning: No trained model found. Please train the model first.")
                print("Run: python nba_ai_predictor.py")
    
    def get_top_scorers(self, limit=10) -> List[Dict]:
        """Get top predicted scorers (PPG)"""
        try:
            top_performers = self.predictor.get_top_performers(top_n=limit)
            if top_performers and 'PPG' in top_performers:
                return top_performers['PPG']
            return []
        except Exception as e:
            print(f"Error getting top scorers: {e}")
            return []
    
    def get_top_assists(self, limit=10) -> List[Dict]:
        """Get top predicted assist leaders (APG)"""
        try:
            top_performers = self.predictor.get_top_performers(top_n=limit)
            if top_performers and 'APG' in top_performers:
                return top_performers['APG']
            return []
        except Exception as e:
            print(f"Error getting top assists: {e}")
            return []
    
    def get_top_rebounders(self, limit=10) -> List[Dict]:
        """Get top predicted rebounders (RPG)"""
        try:
            top_performers = self.predictor.get_top_performers(top_n=limit)
            if top_performers and 'RPG' in top_performers:
                return top_performers['RPG']
            return []
        except Exception as e:
            print(f"Error getting top rebounders: {e}")
            return []
    
    def get_breakout_players(self, limit=10) -> List[Dict]:
        """Get players predicted to have breakout seasons"""
        try:
            overperformers = self.predictor.get_overperformers(threshold=5.0, top_n=limit)
            return overperformers if overperformers else []
        except Exception as e:
            print(f"Error getting breakout players: {e}")
            return []
    
    def get_player_outlook(self, player_name: str) -> Optional[Dict]:
        """Get prediction outlook for a specific player"""
        try:
            return self.predictor.get_player_prediction(player_name)
        except Exception as e:
            print(f"Error getting player outlook for {player_name}: {e}")
            return None
    
    def get_all_predictions(self) -> Dict:
        """Get all predictions in one call"""
        try:
            return {
                'top_scorers': self.get_top_scorers(10),
                'top_assists': self.get_top_assists(10),
                'top_rebounders': self.get_top_rebounders(10),
                'breakout_players': self.get_breakout_players(10),
                'timestamp': self._get_timestamp()
            }
        except Exception as e:
            print(f"Error getting all predictions: {e}")
            return {}
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

# Global instance for easy import
ai_predictions = AIPredictions()

# Convenience functions for direct import
def get_top_scorers(limit=10):
    return ai_predictions.get_top_scorers(limit)

def get_top_assists(limit=10):
    return ai_predictions.get_top_assists(limit)

def get_top_rebounders(limit=10):
    return ai_predictions.get_top_rebounders(limit)

def get_breakout_players(limit=10):
    return ai_predictions.get_breakout_players(limit)

def get_player_outlook(player_name):
    return ai_predictions.get_player_outlook(player_name)

def get_all_predictions():
    return ai_predictions.get_all_predictions()

if __name__ == "__main__":
    # Test the predictions
    print("🏀 Testing AI Predictions...")
    
    print("\nTop 5 Scorers:")
    scorers = get_top_scorers(5)
    for scorer in scorers:
        print(f"{scorer['rank']}. {scorer['name']} ({scorer['team']}) - {scorer['predicted_value']} PPG")
    
    print("\nTop 5 Assist Leaders:")
    assists = get_top_assists(5)
    for assist in assists:
        print(f"{assist['rank']}. {assist['name']} ({assist['team']}) - {assist['predicted_value']} APG")
    
    print("\nTop 5 Rebounders:")
    rebounders = get_top_rebounders(5)
    for rebounder in rebounders:
        print(f"{rebounder['rank']}. {rebounder['name']} ({rebounder['team']}) - {rebounder['predicted_value']} RPG")
    
    print("\nTop 5 Breakout Players:")
    breakouts = get_breakout_players(5)
    for breakout in breakouts:
        print(f"{breakout['rank']}. {breakout['name']} ({breakout['team']}) - {breakout['total_improvement']}% improvement")
