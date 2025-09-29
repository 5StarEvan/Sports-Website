"""
NBA AI Predictor - Main integration script
Combines data collection, model training, and prediction functionality
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import json

# Import our custom modules
from nba_data_collector import NBADataCollector
from nba_pytorch_model import NBAPerformanceAnalyzer
import main  # Import existing main module for NBA API functions

class NBAAIPredictor:
    """Main class that integrates all NBA prediction functionality"""
    
    def __init__(self):
        self.data_collector = NBADataCollector()
        self.analyzer = NBAPerformanceAnalyzer()
        self.model_trained = False
        
    def collect_and_train(self, max_players=150, force_retrain=False):
        """Collect data and train the model"""
        print("=== NBA AI Predictor - Data Collection & Training ===")
        
        # Check if model already exists
        model_file = os.path.join(os.path.dirname(__file__), 'nba_model.pkl')
        data_file = os.path.join(os.path.dirname(__file__), 'nba_player_data.pkl')
        
        if os.path.exists(model_file) and not force_retrain:
            print("Model already exists. Use force_retrain=True to retrain.")
            self.model_trained = True
            return True
        
        # Collect data
        print("Step 1: Collecting NBA player data...")
        data = self.data_collector.load_data()
        
        if data is None or force_retrain:
            print("Collecting fresh data...")
            data = self.data_collector.collect_all_data(max_players=max_players)
            if data:
                self.data_collector.save_data(data)
            else:
                print("Failed to collect data!")
                return False
        
        # Train model
        print("Step 2: Training PyTorch model...")
        success = self.analyzer.train_model()
        
        if success:
            self.model_trained = True
            print("✅ Model training completed successfully!")
            return True
        else:
            print("❌ Model training failed!")
            return False
    
    def get_top_performers(self, top_n=10):
        """Get predictions for top performers in PPG, APG, RPG"""
        if not self.model_trained:
            if not self.analyzer.load_model():
                print("Please train the model first!")
                return None
        
        print(f"\n=== TOP {top_n} PERFORMERS PREDICTION ===")
        top_performers = self.analyzer.predict_top_performers(top_n=top_n)
        
        results = {}
        for stat, players in top_performers.items():
            print(f"\n🏀 Top {top_n} {stat} Predictions:")
            stat_results = []
            for i, (_, player) in enumerate(players.iterrows(), 1):
                print(f"{i:2d}. {player['PLAYER_NAME']} ({player['TEAM']}) - {player[f'PREDICTED_{stat}']:.2f}")
                stat_results.append({
                    'rank': i,
                    'name': player['PLAYER_NAME'],
                    'team': player['TEAM'],
                    'position': player['POSITION'],
                    'age': player['AGE'],
                    'predicted_value': round(player[f'PREDICTED_{stat}'], 2)
                })
            results[stat] = stat_results
        
        return results
    
    def get_overperformers(self, threshold=5.0, top_n=15):
        """Find players predicted to overperform compared to last season"""
        if not self.model_trained:
            if not self.analyzer.load_model():
                print("Please train the model first!")
                return None
        
        print(f"\n=== OVERPERFORMERS ANALYSIS (>{threshold}% improvement) ===")
        overperformers = self.analyzer.find_overperformers(threshold=threshold)
        
        print(f"\n🚀 Top {top_n} Players Predicted to Overperform:")
        results = []
        
        for i, (_, player) in enumerate(overperformers.head(top_n).iterrows(), 1):
            print(f"{i:2d}. {player['PLAYER_NAME']} ({player['TEAM']})")
            print(f"    PPG: {player['PPG_LAST']:.1f} → {player['PREDICTED_PPG']:.1f} ({player['PPG_IMPROVEMENT']:+.1f}%)")
            print(f"    APG: {player['APG_LAST']:.1f} → {player['PREDICTED_APG']:.1f} ({player['APG_IMPROVEMENT']:+.1f}%)")
            print(f"    RPG: {player['RPG_LAST']:.1f} → {player['PREDICTED_RPG']:.1f} ({player['RPG_IMPROVEMENT']:+.1f}%)")
            print(f"    Total Improvement: {player['TOTAL_IMPROVEMENT']:.1f}%")
            print()
            
            results.append({
                'rank': i,
                'name': player['PLAYER_NAME'],
                'team': player['TEAM'],
                'position': player['POSITION'],
                'current_ppg': round(player['PPG_LAST'], 1),
                'predicted_ppg': round(player['PREDICTED_PPG'], 1),
                'ppg_improvement': round(player['PPG_IMPROVEMENT'], 1),
                'current_apg': round(player['APG_LAST'], 1),
                'predicted_apg': round(player['PREDICTED_APG'], 1),
                'apg_improvement': round(player['APG_IMPROVEMENT'], 1),
                'current_rpg': round(player['RPG_LAST'], 1),
                'predicted_rpg': round(player['PREDICTED_RPG'], 1),
                'rpg_improvement': round(player['RPG_IMPROVEMENT'], 1),
                'total_improvement': round(player['TOTAL_IMPROVEMENT'], 1)
            })
        
        return results
    
    def get_player_prediction(self, player_name):
        """Get prediction for a specific player"""
        if not self.model_trained:
            if not self.analyzer.load_model():
                print("Please train the model first!")
                return None
        
        # Load data to find player
        data_file = os.path.join(os.path.dirname(__file__), 'nba_player_data.pkl')
        with open(data_file, 'rb') as f:
            import pickle
            data = pickle.load(f)
        
        df = pd.DataFrame(data)
        player_data = df[df['PLAYER_NAME'].str.contains(player_name, case=False, na=False)]
        
        if player_data.empty:
            print(f"Player '{player_name}' not found in dataset.")
            return None
        
        player = player_data.iloc[0]
        
        # Get prediction using the model
        df_processed = df.fillna(0)
        
        # Encode categorical variables
        for col, le in self.analyzer.trainer.label_encoders.items():
            if col in df_processed.columns:
                df_processed[col] = le.transform(df_processed[col].astype(str))
        
        # Select features for this player
        player_features = df_processed[df_processed['PLAYER_NAME'] == player['PLAYER_NAME']]
        if player_features.empty:
            print("Player data not found in processed dataset.")
            return None
        
        X = player_features[self.analyzer.trainer.feature_columns].values
        X_scaled = self.analyzer.trainer.scaler.transform(X)
        
        # Make prediction
        predictions = self.analyzer.trainer.predict(X_scaled)
        
        print(f"\n=== PREDICTION FOR {player['PLAYER_NAME'].upper()} ===")
        print(f"Team: {player['TEAM']}")
        print(f"Position: {player['POSITION']}")
        print(f"Age: {player['AGE']}")
        print()
        print("Current Season Stats:")
        print(f"  PPG: {player['PPG_LAST']:.1f}")
        print(f"  APG: {player['APG_LAST']:.1f}")
        print(f"  RPG: {player['RPG_LAST']:.1f}")
        print()
        print("Predicted Next Season Stats:")
        print(f"  PPG: {predictions[0][0]:.1f} ({((predictions[0][0] - player['PPG_LAST']) / player['PPG_LAST'] * 100):+.1f}%)")
        print(f"  APG: {predictions[0][1]:.1f} ({((predictions[0][1] - player['APG_LAST']) / player['APG_LAST'] * 100):+.1f}%)")
        print(f"  RPG: {predictions[0][2]:.1f} ({((predictions[0][2] - player['RPG_LAST']) / player['RPG_LAST'] * 100):+.1f}%)")
        
        return {
            'name': player['PLAYER_NAME'],
            'team': player['TEAM'],
            'position': player['POSITION'],
            'age': player['AGE'],
            'current_stats': {
                'ppg': round(player['PPG_LAST'], 1),
                'apg': round(player['APG_LAST'], 1),
                'rpg': round(player['RPG_LAST'], 1)
            },
            'predicted_stats': {
                'ppg': round(predictions[0][0], 1),
                'apg': round(predictions[0][1], 1),
                'rpg': round(predictions[0][2], 1)
            },
            'improvements': {
                'ppg': round(((predictions[0][0] - player['PPG_LAST']) / player['PPG_LAST'] * 100), 1),
                'apg': round(((predictions[0][1] - player['APG_LAST']) / player['APG_LAST'] * 100), 1),
                'rpg': round(((predictions[0][2] - player['RPG_LAST']) / player['RPG_LAST'] * 100), 1)
            }
        }
    
    def generate_report(self, output_file='nba_predictions_report.json'):
        """Generate a comprehensive prediction report"""
        if not self.model_trained:
            if not self.analyzer.load_model():
                print("Please train the model first!")
                return None
        
        print("\n=== GENERATING COMPREHENSIVE REPORT ===")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'model_info': {
                'type': 'PyTorch Neural Network',
                'features': len(self.analyzer.trainer.feature_columns),
                'architecture': 'Multi-layer perceptron with batch normalization and dropout'
            },
            'top_performers': self.get_top_performers(top_n=10),
            'overperformers': self.get_overperformers(threshold=5.0, top_n=15)
        }
        
        # Save report
        output_path = os.path.join(os.path.dirname(__file__), output_file)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Report saved to {output_path}")
        return report

def main_menu():
    """Interactive main menu for the NBA AI Predictor"""
    predictor = NBAAIPredictor()
    
    while True:
        print("\n" + "="*50)
        print("🏀 NBA AI PREDICTOR")
        print("="*50)
        print("1. Collect Data & Train Model")
        print("2. Get Top Performers Prediction")
        print("3. Find Overperformers")
        print("4. Get Player-Specific Prediction")
        print("5. Generate Full Report")
        print("6. Exit")
        print("-"*50)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            force_retrain = input("Force retrain existing model? (y/n): ").lower() == 'y'
            predictor.collect_and_train(force_retrain=force_retrain)
            
        elif choice == '2':
            top_n = int(input("Number of top performers to show (default 10): ") or "10")
            predictor.get_top_performers(top_n=top_n)
            
        elif choice == '3':
            threshold = float(input("Improvement threshold % (default 5.0): ") or "5.0")
            top_n = int(input("Number of overperformers to show (default 15): ") or "15")
            predictor.get_overperformers(threshold=threshold, top_n=top_n)
            
        elif choice == '4':
            player_name = input("Enter player name: ").strip()
            if player_name:
                predictor.get_player_prediction(player_name)
                
        elif choice == '5':
            predictor.generate_report()
            
        elif choice == '6':
            print("Goodbye! 🏀")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--menu':
        main_menu()
    else:
        # Quick demo
        predictor = NBAAIPredictor()
        
        print("🏀 NBA AI Predictor - Quick Demo")
        print("="*40)
        
        # Try to load existing model or train new one
        if not predictor.analyzer.load_model():
            print("No existing model found. Training new model...")
            predictor.collect_and_train(max_players=100)
        
        if predictor.model_trained or predictor.analyzer.load_model():
            # Show top performers
            predictor.get_top_performers(top_n=5)
            
            # Show overperformers
            predictor.get_overperformers(threshold=3.0, top_n=10)
            
            print("\n" + "="*40)
            print("Demo completed! Use --menu flag for interactive mode.")
            print("Example: python nba_ai_predictor.py --menu")
