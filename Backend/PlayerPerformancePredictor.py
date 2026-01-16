import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from nba_api.stats.endpoints import playergamelog, commonplayerinfo
from nba_api.stats.static import teams
import pickle
import os
from datetime import datetime, timedelta
import warnings
from typing import List, Dict, Optional, Tuple, Any
warnings.filterwarnings('ignore')

class PlayerPerformancePredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_file = 'player_performance_model.pkl'
        self.scaler_file = 'player_performance_scaler.pkl'
        
    def load_model(self):
        """Load pre-trained model if it exists"""
        if os.path.exists(self.model_file) and os.path.exists(self.scaler_file):
            try:
                with open(self.model_file, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.scaler_file, 'rb') as f:
                    self.scaler = pickle.load(f)
                self.is_trained = True
                print("Loaded pre-trained model successfully!")
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
        return False
    
    def save_model(self):
        """Save the trained model"""
        try:
            with open(self.model_file, 'wb') as f:
                pickle.dump(self.model, f)
            with open(self.scaler_file, 'wb') as f:
                pickle.dump(self.scaler, f)
            print("Model saved successfully!")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def get_team_id_by_name(self, team_name):
        """Get team ID by team name"""
        team_list = teams.find_teams_by_full_name(team_name)
        if team_list:
            return team_list[0]['id']
        return None
    
    def get_player_games_against_team(self, player_id, team_id, last_n_games=10):
        """Get player's recent games against a specific team"""
        try:
            # Get current season games
            current_season = datetime.now().year
            if datetime.now().month < 7:  # Before July, use previous year as season start
                current_season -= 1
                
            game_log = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=f"{current_season}-{str(current_season + 1)[-2:]}",
                last_n_games=50  # Get more games to filter by opponent
            )
            
            games_data = game_log.get_dict()
            if not games_data['resultSets']:
                return []
            
            headers = games_data['resultSets'][0]['headers']
            games = games_data['resultSets'][0]['rowSet']
            
            # Filter games against the specific team
            games_against_team = []
            for game in games:
                if len(game) > len(headers):
                    continue
                    
                game_dict = dict(zip(headers, game))
                if 'MATCHUP' in game_dict and str(team_id) in str(game_dict.get('MATCHUP', '')):
                    games_against_team.append(game_dict)
            
            return games_against_team[-last_n_games:]  # Return last N games
            
        except Exception as e:
            print(f"Error getting games against team: {e}")
            return []
    
    def calculate_historical_performance_features(self, player_id, opponent_team_id):
        """Calculate historical performance features against opponent team"""
        games_against_team = self.get_player_games_against_team(player_id, opponent_team_id, last_n_games=10)
        
        if not games_against_team:
            # Return default values if no historical data
            return {
                'avg_pts_vs_team': 15.0,
                'avg_ast_vs_team': 3.0,
                'avg_reb_vs_team': 5.0,
                'avg_fg_pct_vs_team': 0.45,
                'games_played_vs_team': 0,
                'last_game_pts': 15.0,
                'last_game_ast': 3.0,
                'last_game_reb': 5.0
            }
        
        # Calculate averages
        pts_list = [float(game.get('PTS', 0)) for game in games_against_team]
        ast_list = [float(game.get('AST', 0)) for game in games_against_team]
        reb_list = [float(game.get('REB', 0)) for game in games_against_team]
        fg_pct_list = [float(game.get('FG_PCT', 0.45)) for game in games_against_team]
        
        # Get last game stats
        last_game = games_against_team[-1]
        
        return {
            'avg_pts_vs_team': np.mean(pts_list),
            'avg_ast_vs_team': np.mean(ast_list),
            'avg_reb_vs_team': np.mean(reb_list),
            'avg_fg_pct_vs_team': np.mean(fg_pct_list),
            'games_played_vs_team': len(games_against_team),
            'last_game_pts': float(last_game.get('PTS', 15.0)),
            'last_game_ast': float(last_game.get('AST', 3.0)),
            'last_game_reb': float(last_game.get('REB', 5.0))
        }
    
    def create_player_features(self, player_obj, opponent_team_name):
        """Create feature vector for a player"""
        opponent_team_id = self.get_team_id_by_name(opponent_team_name)
        player_id = self.get_player_id_by_name(player_obj.name)
        
        # Get historical performance against opponent
        historical_features = self.calculate_historical_performance_features(player_id, opponent_team_id) if player_id else {
            'avg_pts_vs_team': 15.0,
            'avg_ast_vs_team': 3.0,
            'avg_reb_vs_team': 5.0,
            'avg_fg_pct_vs_team': 0.45,
            'games_played_vs_team': 0,
            'last_game_pts': 15.0,
            'last_game_ast': 3.0,
            'last_game_reb': 5.0
        }
        
        # Create feature vector
        features = [
            player_obj.age,
            player_obj.ppg,
            player_obj.apg,
            player_obj.rpg,
            player_obj.spg,
            player_obj.bpg,
            player_obj.tpg,
            player_obj.fpg,
            player_obj.fgptc / 100.0,  # Convert percentage to decimal
            historical_features['avg_pts_vs_team'],
            historical_features['avg_ast_vs_team'],
            historical_features['avg_reb_vs_team'],
            historical_features['avg_fg_pct_vs_team'],
            historical_features['games_played_vs_team'],
            historical_features['last_game_pts'],
            historical_features['last_game_ast'],
            historical_features['last_game_reb']
        ]
        
        return np.array(features)
    
    def generate_training_data(self, sample_size=1000):
        """Generate synthetic training data based on realistic NBA player distributions"""
        np.random.seed(42)
        
        # Define realistic ranges for NBA players
        age_range = (19, 40)
        ppg_range = (5, 35)
        apg_range = (1, 12)
        rpg_range = (1, 15)
        spg_range = (0.5, 3)
        bpg_range = (0.1, 4)
        tpg_range = (1, 5)
        fpg_range = (1, 10)
        fg_pct_range = (0.35, 0.65)
        
        training_data = []
        training_labels = []
        
        for _ in range(sample_size):
            # Generate random player stats
            age = np.random.uniform(age_range[0], age_range[1])
            ppg = np.random.uniform(ppg_range[0], ppg_range[1])
            apg = np.random.uniform(apg_range[0], apg_range[1])
            rpg = np.random.uniform(rpg_range[0], rpg_range[1])
            spg = np.random.uniform(spg_range[0], spg_range[1])
            bpg = np.random.uniform(bpg_range[0], bpg_range[1])
            tpg = np.random.uniform(tpg_range[0], tpg_range[1])
            fpg = np.random.uniform(fpg_range[0], fpg_range[1])
            fg_pct = np.random.uniform(fg_pct_range[0], fg_pct_range[1])
            
            # Generate historical performance features
            avg_pts_vs_team = ppg * np.random.uniform(0.7, 1.3)  # Vary around career average
            avg_ast_vs_team = apg * np.random.uniform(0.7, 1.3)
            avg_reb_vs_team = rpg * np.random.uniform(0.7, 1.3)
            avg_fg_pct_vs_team = fg_pct * np.random.uniform(0.8, 1.2)
            games_played_vs_team = np.random.randint(1, 20)
            last_game_pts = avg_pts_vs_team * np.random.uniform(0.5, 1.5)
            last_game_ast = avg_ast_vs_team * np.random.uniform(0.5, 1.5)
            last_game_reb = avg_reb_vs_team * np.random.uniform(0.5, 1.5)
            
            # Create feature vector
            features = [
                age, ppg, apg, rpg, spg, bpg, tpg, fpg, fg_pct,
                avg_pts_vs_team, avg_ast_vs_team, avg_reb_vs_team, avg_fg_pct_vs_team,
                games_played_vs_team, last_game_pts, last_game_ast, last_game_reb
            ]
            
            # Generate realistic rating (5 is normal, 10 is exceptional, 1 is poor)
            # Base rating on overall performance
            base_rating = 5.0
            
            # Adjust based on scoring efficiency
            if ppg > 25 and fg_pct > 0.5:
                base_rating += 1.5
            elif ppg > 20 and fg_pct > 0.45:
                base_rating += 1.0
            elif ppg < 10 or fg_pct < 0.4:
                base_rating -= 1.0
            
            # Adjust based on historical performance against team
            if avg_pts_vs_team > ppg * 1.1:
                base_rating += 0.5
            elif avg_pts_vs_team < ppg * 0.9:
                base_rating -= 0.5
            
            # Adjust based on recent form
            if last_game_pts > avg_pts_vs_team * 1.2:
                base_rating += 0.3
            elif last_game_pts < avg_pts_vs_team * 0.8:
                base_rating -= 0.3
            
            # Add some randomness
            base_rating += np.random.normal(0, 0.5)
            
            # Clamp to 1-10 range
            rating = np.clip(base_rating, 1.0, 10.0)
            
            training_data.append(features)
            training_labels.append(rating)
        
        return np.array(training_data), np.array(training_labels)
    
    def train_model(self, use_synthetic_data=True):
        """Train the performance prediction model"""
        if use_synthetic_data:
            print("Generating synthetic training data...")
            X, y = self.generate_training_data(sample_size=2000)
        else:
            # TODO: Implement real data training
            print("Real data training not implemented yet. Using synthetic data.")
            X, y = self.generate_training_data(sample_size=2000)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        print("Training Random Forest model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model Performance:")
        print(f"Mean Squared Error: {mse:.3f}")
        print(f"R² Score: {r2:.3f}")
        print(f"Average prediction error: {np.sqrt(mse):.2f} points")
        
        self.is_trained = True
        self.save_model()
        
        return mse, r2
    
    def predict_performance_rating(self, player_obj, opponent_team_name):
        """Predict performance rating (1-10) for a player against a specific team"""
        if not self.is_trained:
            print("Model not trained. Training now...")
            self.train_model()
        
        # Create feature vector
        features = self.create_player_features(player_obj, opponent_team_name)
        
        # Scale features
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Make prediction
        rating = self.model.predict(features_scaled)[0]
        
        # Clamp to 1-10 range
        rating = np.clip(rating, 1.0, 10.0)
        
        return round(rating, 2)
    
    def get_player_id_by_name(self, player_name):
        """Get player ID by name"""
        from nba_api.stats.static import players
        player_list = players.find_players_by_full_name(player_name)
        if player_list:
            return player_list[0]['id']
        return None
    
    def analyze_player_performance(self, player_obj, opponent_team_name):
        """Comprehensive analysis of player performance prediction"""
        rating = self.predict_performance_rating(player_obj, opponent_team_name)
        
        # Get historical data
        player_id = self.get_player_id_by_name(player_obj.name)
        opponent_team_id = self.get_team_id_by_name(opponent_team_name)
        historical_features = self.calculate_historical_performance_features(player_id, opponent_team_id) if player_id else None
        
        analysis = {
            'player_name': player_obj.name,
            'opponent_team': opponent_team_name,
            'predicted_rating': rating,
            'performance_level': self._get_performance_level(rating),
            'current_stats': {
                'ppg': player_obj.ppg,
                'apg': player_obj.apg,
                'rpg': player_obj.rpg,
                'fg_pct': player_obj.fgptc
            },
            'historical_vs_opponent': historical_features
        }
        
        return analysis
    
    def _get_performance_level(self, rating):
        """Convert rating to performance level description"""
        if rating >= 8.5:
            return "Exceptional"
        elif rating >= 7.0:
            return "Very Good"
        elif rating >= 5.5:
            return "Above Average"
        elif rating >= 4.5:
            return "Average"
        elif rating >= 3.0:
            return "Below Average"
        else:
            return "Poor"
    
    def print_analysis(self, analysis):
        """Print formatted analysis results"""
        print(f"\n{'='*60}")
        print(f"PERFORMANCE PREDICTION ANALYSIS")
        print(f"{'='*60}")
        print(f"Player: {analysis['player_name']}")
        print(f"Opponent: {analysis['opponent_team']}")
        print(f"Predicted Rating: {analysis['predicted_rating']}/10")
        print(f"Performance Level: {analysis['performance_level']}")
        
        print(f"\nCurrent Season Stats:")
        stats = analysis['current_stats']
        print(f"  Points per game: {stats['ppg']}")
        print(f"  Assists per game: {stats['apg']}")
        print(f"  Rebounds per game: {stats['rpg']}")
        print(f"  Field Goal %: {stats['fg_pct']}%")
        
        if analysis['historical_vs_opponent']:
            hist = analysis['historical_vs_opponent']
            print(f"\nHistorical Performance vs {analysis['opponent_team']}:")
            print(f"  Games played: {hist['games_played_vs_team']}")
            print(f"  Avg points: {hist['avg_pts_vs_team']:.1f}")
            print(f"  Avg assists: {hist['avg_ast_vs_team']:.1f}")
            print(f"  Avg rebounds: {hist['avg_reb_vs_team']:.1f}")
            print(f"  Avg FG%: {hist['avg_fg_pct_vs_team']:.3f}")
            print(f"  Last game: {hist['last_game_pts']:.1f} pts, {hist['last_game_ast']:.1f} ast, {hist['last_game_reb']:.1f} reb")
        
        print(f"{'='*60}\n")

# Example usage and testing
if __name__ == "__main__":
    # Initialize predictor
    predictor = PlayerPerformancePredictor()
    
    # Try to load existing model, otherwise train new one
    if not predictor.load_model():
        print("Training new model...")
        predictor.train_model()
    
    # Test with a sample player (you would use real player objects from your main.py)
    print("Model ready for predictions!")
    print("Use predictor.predict_performance_rating(player_obj, opponent_team_name) to get ratings.")
    print("Use predictor.analyze_player_performance(player_obj, opponent_team_name) for detailed analysis.")

    # Simple prediction
    rating = predictor.predict_performance_rating(player_obj, "Los Angeles Lakers")

    # Detailed analysis
    analysis = predictor.analyze_player_performance(player_obj, "Los Angeles Lakers")
    predictor.print_analysis(analysis) 