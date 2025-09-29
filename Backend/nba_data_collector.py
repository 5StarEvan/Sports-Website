import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguedashplayerstats, playergamelog, commonplayerinfo
from nba_api.stats.static import players
from datetime import datetime, timedelta
import time
import pickle
import os

class NBADataCollector:
    def __init__(self):
        self.seasons = ['2022-23', '2023-24']  # Past 2 years
        self.player_data = []
        self.game_logs = {}
        
    def get_season_stats(self, season):
        """Get all player stats for a specific season"""
        try:
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=season,
                season_type_all_star='Regular Season',
                per_mode_detailed='PerGame'
            ).get_dict()
            
            headers = stats['resultSets'][0]['headers']
            rows = stats['resultSets'][0]['rowSet']
            
            df = pd.DataFrame(rows, columns=headers)
            df['SEASON'] = season
            return df
            
        except Exception as e:
            print(f"Error fetching season {season}: {e}")
            return None
    
    def get_player_game_logs(self, player_id, season):
        """Get detailed game logs for a player in a specific season"""
        try:
            # Add delay to avoid rate limiting
            time.sleep(0.6)
            
            game_log = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=season,
                season_type_all_star='Regular Season'
            ).get_dict()
            
            if game_log['resultSets'] and game_log['resultSets'][0]['rowSet']:
                headers = game_log['resultSets'][0]['headers']
                rows = game_log['resultSets'][0]['rowSet']
                df = pd.DataFrame(rows, columns=headers)
                return df
            return None
            
        except Exception as e:
            print(f"Error fetching game logs for player {player_id} in {season}: {e}")
            return None
    
    def get_player_info(self, player_id):
        """Get basic player information"""
        try:
            time.sleep(0.6)
            info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_dict()
            
            if info['resultSets'] and info['resultSets'][0]['rowSet']:
                headers = info['resultSets'][0]['headers']
                row = info['resultSets'][0]['rowSet'][0]
                player_info = dict(zip(headers, row))
                return player_info
            return None
            
        except Exception as e:
            print(f"Error fetching player info for {player_id}: {e}")
            return None
    
    def collect_all_data(self, max_players=200):
        """Collect comprehensive data for all players"""
        print("Starting NBA data collection...")
        
        all_season_data = []
        
        # Collect season stats for all seasons
        for season in self.seasons:
            print(f"Collecting data for season {season}...")
            season_data = self.get_season_stats(season)
            if season_data is not None:
                all_season_data.append(season_data)
                time.sleep(1)  # Rate limiting
        
        if not all_season_data:
            print("No season data collected!")
            return None
        
        # Combine all season data
        combined_data = pd.concat(all_season_data, ignore_index=True)
        
        # Get unique players (limit to top players by games played)
        top_players = combined_data.nlargest(max_players, 'GP')
        unique_players = top_players['PLAYER_ID'].unique()
        
        print(f"Collecting detailed data for {len(unique_players)} players...")
        
        detailed_data = []
        
        for i, player_id in enumerate(unique_players):
            if i % 10 == 0:
                print(f"Processing player {i+1}/{len(unique_players)}")
            
            # Get player info
            player_info = self.get_player_info(player_id)
            if not player_info:
                continue
            
            # Get game logs for each season
            player_seasons = []
            for season in self.seasons:
                game_logs = self.get_player_game_logs(player_id, season)
                if game_logs is not None and len(game_logs) > 10:  # Only include players with sufficient data
                    game_logs['SEASON'] = season
                    player_seasons.append(game_logs)
            
            if player_seasons:
                # Combine all seasons for this player
                player_all_logs = pd.concat(player_seasons, ignore_index=True)
                
                # Calculate rolling averages and trends
                player_data = self.calculate_player_features(player_all_logs, player_info)
                if player_data:
                    detailed_data.append(player_data)
        
        print(f"Collected detailed data for {len(detailed_data)} players")
        return detailed_data
    
    def calculate_player_features(self, game_logs, player_info):
        """Calculate advanced features from game logs"""
        try:
            # Sort by date
            game_logs['GAME_DATE'] = pd.to_datetime(game_logs['GAME_DATE'])
            game_logs = game_logs.sort_values('GAME_DATE')
            
            # Basic stats
            features = {
                'PLAYER_ID': player_info.get('PERSON_ID'),
                'PLAYER_NAME': player_info.get('DISPLAY_FIRST_LAST'),
                'HEIGHT': self.parse_height(player_info.get('HEIGHT', '0-0')),
                'WEIGHT': player_info.get('WEIGHT', 0),
                'AGE': self.calculate_age(player_info.get('BIRTHDATE')),
                'POSITION': player_info.get('POSITION', ''),
                'TEAM': game_logs['MATCHUP'].iloc[-1].split(' ')[0] if len(game_logs) > 0 else '',
            }
            
            # Per-game stats (last season)
            last_season = game_logs[game_logs['SEASON'] == game_logs['SEASON'].iloc[-1]]
            if len(last_season) > 0:
                features.update({
                    'PPG_LAST': last_season['PTS'].mean(),
                    'APG_LAST': last_season['AST'].mean(),
                    'RPG_LAST': last_season['REB'].mean(),
                    'SPG_LAST': last_season['STL'].mean(),
                    'BPG_LAST': last_season['BLK'].mean(),
                    'TOV_LAST': last_season['TOV'].mean(),
                    'FG_PCT_LAST': last_season['FG_PCT'].mean(),
                    'FG3_PCT_LAST': last_season['FG3_PCT'].mean(),
                    'FT_PCT_LAST': last_season['FT_PCT'].mean(),
                    'MIN_LAST': last_season['MIN'].mean(),
                    'GAMES_PLAYED_LAST': len(last_season),
                })
            
            # Previous season stats
            if len(game_logs['SEASON'].unique()) > 1:
                prev_season = game_logs[game_logs['SEASON'] == game_logs['SEASON'].unique()[-2]]
                if len(prev_season) > 0:
                    features.update({
                        'PPG_PREV': prev_season['PTS'].mean(),
                        'APG_PREV': prev_season['AST'].mean(),
                        'RPG_PREV': prev_season['REB'].mean(),
                        'SPG_PREV': prev_season['STL'].mean(),
                        'BPG_PREV': prev_season['BLK'].mean(),
                        'TOV_PREV': prev_season['TOV'].mean(),
                        'FG_PCT_PREV': prev_season['FG_PCT'].mean(),
                        'FG3_PCT_PREV': prev_season['FG3_PCT'].mean(),
                        'FT_PCT_PREV': prev_season['FT_PCT'].mean(),
                        'MIN_PREV': prev_season['MIN'].mean(),
                        'GAMES_PLAYED_PREV': len(prev_season),
                    })
            
            # Rolling averages and trends
            if len(game_logs) >= 10:
                # Last 10 games
                last_10 = game_logs.tail(10)
                features.update({
                    'PPG_LAST_10': last_10['PTS'].mean(),
                    'APG_LAST_10': last_10['AST'].mean(),
                    'RPG_LAST_10': last_10['REB'].mean(),
                    'FG_PCT_LAST_10': last_10['FG_PCT'].mean(),
                })
                
                # Trend analysis
                if len(game_logs) >= 20:
                    first_half = game_logs.head(len(game_logs)//2)
                    second_half = game_logs.tail(len(game_logs)//2)
                    
                    features.update({
                        'PPG_TREND': second_half['PTS'].mean() - first_half['PTS'].mean(),
                        'APG_TREND': second_half['AST'].mean() - first_half['AST'].mean(),
                        'RPG_TREND': second_half['REB'].mean() - first_half['REB'].mean(),
                    })
            
            # Consistency metrics
            if len(game_logs) > 5:
                features.update({
                    'PPG_STD': game_logs['PTS'].std(),
                    'APG_STD': game_logs['AST'].std(),
                    'RPG_STD': game_logs['REB'].std(),
                    'CONSISTENCY_SCORE': 1 / (1 + game_logs['PTS'].std()),  # Higher is more consistent
                })
            
            return features
            
        except Exception as e:
            print(f"Error calculating features: {e}")
            return None
    
    def parse_height(self, height_str):
        """Parse height string to inches"""
        try:
            if '-' in height_str:
                feet, inches = height_str.split('-')
                return int(feet) * 12 + int(inches)
            return 0
        except:
            return 0
    
    def calculate_age(self, birthdate_str):
        """Calculate age from birthdate"""
        try:
            if birthdate_str:
                birth_date = datetime.strptime(birthdate_str.split('T')[0], '%Y-%m-%d')
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                return age
            return 0
        except:
            return 0
    
    def save_data(self, data, filename='nba_player_data.pkl'):
        """Save collected data to file"""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"Data saved to {filepath}")
    
    def load_data(self, filename='nba_player_data.pkl'):
        """Load data from file"""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            print(f"Data loaded from {filepath}")
            return data
        return None

if __name__ == "__main__":
    collector = NBADataCollector()
    
    # Try to load existing data first
    data = collector.load_data()
    
    if data is None:
        print("No existing data found. Collecting new data...")
        data = collector.collect_all_data(max_players=150)
        if data:
            collector.save_data(data)
    
    if data:
        print(f"Successfully loaded data for {len(data)} players")
        # Convert to DataFrame for analysis
        df = pd.DataFrame(data)
        print(f"Data shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nSample data:")
        print(df.head())
