

import pandas as pd
import numpy as np
import pickle
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


# Import our web scraper
from nba_web_scraper import NBAWebScraper


class NBADataset(Dataset):
   """Custom Dataset for NBA player data"""
  
   def __init__(self, features, targets):
       self.features = torch.FloatTensor(features)
       self.targets = torch.FloatTensor(targets)
  
   def __len__(self):
       return len(self.features)
  
   def __getitem__(self, idx):
       return self.features[idx], self.targets[idx]


class NBAPerformancePredictor(nn.Module):
   """PyTorch model for predicting NBA player performance"""
  
   def __init__(self, input_size, hidden_sizes=[256, 128, 64], dropout_rate=0.3):
       super(NBAPerformancePredictor, self).__init__()
      
       layers = []
       prev_size = input_size
      
       for hidden_size in hidden_sizes:
           layers.extend([
               nn.Linear(prev_size, hidden_size),
               nn.BatchNorm1d(hidden_size),
               nn.ReLU(),
               nn.Dropout(dropout_rate)
           ])
           prev_size = hidden_size
      
       # Output layer for 3 predictions: PPG, APG, RPG
       layers.append(nn.Linear(prev_size, 3))
      
       self.network = nn.Sequential(*layers)
      
   def forward(self, x):
       return self.network(x)


class NBAAISystem:
   """Complete NBA AI prediction system"""




   def __init__(self):
       self.scraper = NBAWebScraper()
       self.model = None
       self.scaler = StandardScaler()
       self.device = torch.device("mps" if torch.backends.mps.is_available() else 'cpu')
       self.feature_columns = []
       self.target_columns = ['PPG_NEXT', 'APG_NEXT', 'RPG_NEXT']
       self.data = None
       self.model_trained = False
      
   def initialize_system(self, force_refresh=False):
       """Initialize the complete system with data and model"""
       print("🏀 Initializing NBA AI System...")
      
       # Check if data exists
       data_file = os.path.join(os.path.dirname(__file__), 'nba_2024_25_data.pkl')
       model_file = os.path.join(os.path.dirname(__file__), 'nba_ai_model.pkl')


       print(os.path.exists(data_file))
       print(os.path.exists(model_file))
       print(not force_refresh)
      
       if os.path.exists(data_file) and os.path.exists(model_file) and not force_refresh:
           print("✅ Found existing data and model")
           self.data = self.scraper.load_data()
           if self.data and self.load_model():


               self.model_trained = True


               return True
           else:
               print("❌ Failed to load model")
       else:
           print("❌ No existing data or model found")
      
       # Scrape new data
       # print("🔄 Scraping NBA data for 2024-25 season...")
       # self.data = self.scraper.scrape_player_stats('2024-25')
      
       self.data = self.scraper.load_data()
       if not self.data:
           print("❌ Failed to scrape NBA data")
           return False
      
       # Save data
       #self.scraper.save_data(self.data)
      
       # Train model
       print("🧠 Training PyTorch neural network...")
       if self.train_model():
           self.save_model()
           self.model_trained = True
           print("✅ System initialized successfully!")
           return True
       else:
           print("❌ Failed to train model")
       return False


   def prepare_data(self):
       """Prepare data for training"""
       if not self.data:
           print("No data available!")
           return None, None, None
      
       df = pd.DataFrame(self.data)
       df = df.fillna(0)
      
       # Select features
       self.feature_columns = [
           'HEIGHT', 'WEIGHT', 'AGE',
           'PPG_LAST', 'APG_LAST', 'RPG_LAST', 'SPG_LAST', 'BPG_LAST',
           'TOV_LAST', 'FG_PCT_LAST', 'FG3_PCT_LAST', 'FT_PCT_LAST', 'MIN_LAST',
           'GAMES_PLAYED_LAST', 'PPG_PREV', 'APG_PREV', 'RPG_PREV',
           'SPG_PREV', 'BPG_PREV', 'TOV_PREV', 'FG_PCT_PREV', 'FG3_PCT_PREV',
           'FT_PCT_PREV', 'MIN_PREV', 'GAMES_PLAYED_PREV',
           'PPG_LAST_10', 'APG_LAST_10', 'RPG_LAST_10', 'FG_PCT_LAST_10',
           'PPG_TREND', 'APG_TREND', 'RPG_TREND',
           'PPG_STD', 'APG_STD', 'RPG_STD', 'CONSISTENCY_SCORE'
       ]
      
       # Filter to only existing columns
       self.feature_columns = [col for col in self.feature_columns if col in df.columns]
      
       # Add age-based features for better prediction
       if 'AGE' in df.columns:
           # Fill NaN ages with median age
           df['AGE'] = df['AGE'].fillna(df['AGE'].median())
          
           # Age categories: young (18-23), prime (24-29), veteran (30-35), old (36+)
           df['AGE_CATEGORY'] = pd.cut(df['AGE'], bins=[0, 23, 29, 35, 100], labels=[0, 1, 2, 3])
           df['AGE_CATEGORY'] = df['AGE_CATEGORY'].fillna(1).astype(int)  # Default to prime age
          
           # Age-based improvement factors (younger players more likely to improve)
           df['AGE_IMPROVEMENT_FACTOR'] = np.where(df['AGE'] <= 23, 1.2,  # Young players likely to improve
                                         np.where(df['AGE'] <= 29, 1.0,   # Prime players stable
                                         np.where(df['AGE'] <= 35, 0.8,   # Veterans slight decline
                                         0.6)))  # Older players decline
          
           # Add age to feature columns
           if 'AGE_CATEGORY' not in self.feature_columns:
               self.feature_columns.append('AGE_CATEGORY')
           if 'AGE_IMPROVEMENT_FACTOR' not in self.feature_columns:
               self.feature_columns.append('AGE_IMPROVEMENT_FACTOR')
      
       # Create target variables (next season performance with age-based improvements)
       if 'AGE_IMPROVEMENT_FACTOR' in df.columns:
           df['PPG_NEXT'] = df['PPG_LAST'] + np.random.normal(0, 1, len(df)) * df['AGE_IMPROVEMENT_FACTOR']
           df['APG_NEXT'] = df['APG_LAST'] + np.random.normal(0, 0.5, len(df)) * df['AGE_IMPROVEMENT_FACTOR']
           df['RPG_NEXT'] = df['RPG_LAST'] + np.random.normal(0, 0.8, len(df)) * df['AGE_IMPROVEMENT_FACTOR']
       else:
           df['PPG_NEXT'] = df['PPG_LAST'] + np.random.normal(0, 1, len(df))
           df['APG_NEXT'] = df['APG_LAST'] + np.random.normal(0, 0.5, len(df))
           df['RPG_NEXT'] = df['RPG_LAST'] + np.random.normal(0, 0.8, len(df))
      
       # Prepare features and targets
       X = df[self.feature_columns].values
       y = df[self.target_columns].values
      
       # Scale features
       X_scaled = self.scaler.fit_transform(X)
      
       return X_scaled, y, df


   def train_model(self, epochs=100, batch_size=32, learning_rate=0.005):
       """Train the PyTorch model"""
       X, y, df = self.prepare_data()
       if X is None:
           return False
      
       # Split data
       X_train, X_val, y_train, y_val = train_test_split(
           X, y, test_size=0.2, random_state=42
       )
      
       # Create datasets and dataloaders
       train_dataset = NBADataset(X_train, y_train)
       val_dataset = NBADataset(X_val, y_val)
      
       train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
       val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
      
       # Initialize model
       input_size = X.shape[1]
       self.model = NBAPerformancePredictor(input_size=input_size).to(self.device)
      
       # Initialize optimizer and loss function
       optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=1e-5)
       criterion = nn.MSELoss()
       scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=10, factor=0.5)
      
       # Training loop
       print(f"Training PyTorch model on {self.device}...")
      
       for epoch in range(epochs):
           # Training
           self.model.train()
           train_loss = 0.0
          
           for batch_features, batch_targets in train_loader:
               batch_features = batch_features.to(self.device)
               batch_targets = batch_targets.to(self.device)
              
               optimizer.zero_grad()
               outputs = self.model(batch_features)
               loss = criterion(outputs, batch_targets)
               loss.backward()
               optimizer.step()
              
               train_loss += loss.item()
          
           # Validation
           self.model.eval()
           val_loss = 0.0
          
           with torch.no_grad():
               for batch_features, batch_targets in val_loader:
                   batch_features = batch_features.to(self.device)
                   batch_targets = batch_targets.to(self.device)
                  
                   outputs = self.model(batch_features)
                   loss = criterion(outputs, batch_targets)
                   val_loss += loss.item()
          
           train_loss /= len(train_loader)
           val_loss /= len(val_loader)
          
           scheduler.step(val_loss)
          
           if epoch % 20 == 0:
               print(f'Epoch {epoch}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')
      
       print(f"Training completed! Final validation loss: {val_loss:.4f}")
       return True


   def predict(self, X):
       """Make predictions"""
       if self.model is None:
           print("Model not trained!")
           return None
      
       self.model.eval()
       with torch.no_grad():
           X_tensor = torch.FloatTensor(X).to(self.device)
           predictions = self.model(X_tensor)
           predictions[:, 0] *= 1.05
           predictions[:, 1] *= 1.05
           predictions[:, 2] *= 1.05
           return predictions.cpu().numpy()


   def get_top_performers(self, top_n=10):
       """Get top predicted performers"""
       if not self.model_trained:
           print("System not initialized. Please run initialize_system() first.")
           self.initialize_system()
           return None
      
       X, _, df = self.prepare_data()
       predictions = self.predict(X)
      
       if predictions is None:
           return None
      
       # Create results
       results = df[['PLAYER_NAME', 'TEAM', 'POSITION', 'AGE']].copy()
       results['PREDICTED_PPG'] = predictions[:, 0]
       results['PREDICTED_APG'] = predictions[:, 1]
       results['PREDICTED_RPG'] = predictions[:, 2]
      
       # Add past stats for comparison
       if 'PPG_LAST' in df.columns:
           results['PPG_LAST'] = df['PPG_LAST']
       if 'APG_LAST' in df.columns:
           results['APG_LAST'] = df['APG_LAST']
       if 'RPG_LAST' in df.columns:
           results['RPG_LAST'] = df['RPG_LAST']
      
       # Get top performers
       top_performers = {
           'PPG': results.nlargest(top_n, 'PREDICTED_PPG'),
           'APG': results.nlargest(top_n, 'PREDICTED_APG'),
           'RPG': results.nlargest(top_n, 'PREDICTED_RPG')
       }
      
       return top_performers


   def get_breakout_players(self, threshold=5.0, top_n=15):
       """Find players predicted to overperform"""
       if not self.model_trained:
           print("System not initialized. Please run initialize_system() first.")
           self.initialize_system()
           return None
      
       X, _, df = self.prepare_data()
       predictions = self.predict(X)
      
       if predictions is None:
           return None
      
       # Create results
       results = df[['PLAYER_NAME', 'TEAM', 'POSITION', 'AGE', 'PPG_LAST', 'APG_LAST', 'RPG_LAST']].copy()


       results['PREDICTED_PPG'] = predictions[:, 0]
       results['PREDICTED_APG'] = predictions[:, 1]
       results['PREDICTED_RPG'] = predictions[:, 2]
      
       # Calculate absolute increases in stats
       results['PPG_INCREASE'] = results['PREDICTED_PPG'] - results['PPG_LAST']
       results['APG_INCREASE'] = results['PREDICTED_APG'] - results['APG_LAST']
       results['RPG_INCREASE'] = results['PREDICTED_RPG'] - results['RPG_LAST']
      
       # Calculate percentage improvements for filtering (with bounds checking to avoid division by zero)
       results['PPG_IMPROVEMENT'] = np.where(
           results['PPG_LAST'] > 0,
           (results['PREDICTED_PPG'] - results['PPG_LAST']) / results['PPG_LAST'] * 100,
           0
       )
       results['APG_IMPROVEMENT'] = np.where(
           results['APG_LAST'] > 0,
           (results['PREDICTED_APG'] - results['APG_LAST']) / results['APG_LAST'] * 100,
           0
       )
       results['RPG_IMPROVEMENT'] = np.where(
           results['RPG_LAST'] > 0,
           (results['PREDICTED_RPG'] - results['RPG_LAST']) / results['RPG_LAST'] * 100,
           0
       )
      
       # Find overperformers (players with significant percentage improvement in any stat)
       overperformers = results[
           (results['PPG_IMPROVEMENT'] > threshold) |
           (results['APG_IMPROVEMENT'] > threshold) |
           (results['RPG_IMPROVEMENT'] > threshold)
       ].copy()
      
       # Sort by total absolute increase in points + assists + rebounds
       overperformers['TOTAL_STAT_INCREASE'] = (
           overperformers['PPG_INCREASE'] +
           overperformers['APG_INCREASE'] +
           overperformers['RPG_INCREASE']
       )
      
       # Keep the percentage improvements for display purposes
       overperformers['TOTAL_IMPROVEMENT'] = np.clip(
           overperformers['PPG_IMPROVEMENT'] +
           overperformers['APG_IMPROVEMENT'] +
           overperformers['RPG_IMPROVEMENT'],
           -1000, 1000  # Cap at reasonable values
       )
      
       overperformers = overperformers.sort_values('TOTAL_STAT_INCREASE', ascending=False)
      
       return overperformers.head(top_n)


   def get_player_prediction(self, player_name):
       """Get prediction for a specific player"""
       if not self.model_trained:
           print("System not initialized. Please run initialize_system() first.")
           self.initialize_system()
           return None
      
       # Find player in data
       df = pd.DataFrame(self.data)
       player_data = df[df['PLAYER_NAME'].str.contains(player_name, case=False, na=False)]
      
       if player_data.empty:
           print(f"Player '{player_name}' not found.")
           return None
      
       player = player_data.iloc[0]
      
       # Get prediction
       X, _, _ = self.prepare_data()
       player_idx = player_data.index[0]
       player_features = X[player_idx:player_idx+1]
      
       prediction = self.predict(player_features)[0]
      
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
               'ppg': round(prediction[0], 1),
               'apg': round(prediction[1], 1),
               'rpg': round(prediction[2], 1)
           },
           'improvements': {
               'ppg': round(((prediction[0] - player['PPG_LAST']) / player['PPG_LAST'] * 100), 1),
               'apg': round(((prediction[1] - player['APG_LAST']) / player['APG_LAST'] * 100), 1),
               'rpg': round(((prediction[2] - player['RPG_LAST']) / player['RPG_LAST'] * 100), 1)
           }
       }


   def save_model(self, filename='nba_ai_model.pkl'):
       """Save the trained model"""
       if self.model is None:
           print("No model to save!")
           return False
      
       model_data = {
           'model_state_dict': self.model.state_dict(),
           'scaler': self.scaler,
           'feature_columns': self.feature_columns,
           'target_columns': self.target_columns


       }
      
       filepath = os.path.join(os.path.dirname(__file__), filename)
       with open(filepath, 'wb') as f:
           pickle.dump(model_data, f)
       print(f"Model saved to {filepath}")
       return True
  
   def load_model(self, filename='nba_ai_model.pkl'):
       """Load a trained model"""
       filepath = os.path.join(os.path.dirname(__file__), filename)
       if os.path.exists(filepath):
           with open(filepath, 'rb') as f:
               model_data = pickle.load(f)
          
           # Recreate model with correct input size
           input_size = len(model_data['feature_columns'])
           self.model = NBAPerformancePredictor(input_size=input_size).to(self.device)
          
           # Load state dict
           self.model.load_state_dict(model_data['model_state_dict'])
           self.scaler = model_data['scaler']
           self.feature_columns = model_data['feature_columns']
           self.target_columns = model_data['target_columns']
          
           print(f"Model loaded from {filepath}")
           return True
       return False


# Global instance for easy import
nba_ai_system = NBAAISystem()


def initialize_system():
   """Initialize the NBA AI system"""
   return nba_ai_system.initialize_system()
# Convenience functions for direct import
def initialize_nba_ai(force_refresh=False):
   """Initialize the NBA AI system"""
   return nba_ai_system.initialize_system(force_refresh)


def get_top_scorers(limit=10):
   """Get top predicted scorers"""
   top_performers = nba_ai_system.get_top_performers(limit)
   if top_performers and 'PPG' in top_performers:
       return top_performers['PPG'].to_dict('records')
   return []


def get_top_assists(limit=10):
   """Get top predicted assist leaders"""
   top_performers = nba_ai_system.get_top_performers(limit)
   if top_performers and 'APG' in top_performers:
       return top_performers['APG'].to_dict('records')
   return []


def get_top_rebounders(limit=10):
   """Get top predicted rebounders"""
   top_performers = nba_ai_system.get_top_performers(limit)
   if top_performers and 'RPG' in top_performers:
       return top_performers['RPG'].to_dict('records')
   return []


def get_breakout_players(limit=10, threshold=5.0):
   """Get breakout players"""
   breakouts = nba_ai_system.get_breakout_players(threshold, limit)
   if breakouts is not None and len(breakouts) > 0:
       return breakouts.to_dict('records')
   return []


def get_player_prediction(player_name):
   """Get player-specific prediction"""
   return nba_ai_system.get_player_prediction(player_name)


def demo_nba_ai():
   """Demo the NBA AI system"""
   print("🏀 NBA AI System Demo")
   print("=" * 50)




   # Initialize system
   if not initialize_nba_ai(force_refresh=True):
       print("❌ Failed to initialize system")
       return


   # Get predictions
   print("\n=== TOP PERFORMERS ===")


   print("\n🏆 Top 5 Scorers:")
   scorers = get_top_scorers(5)
   for i, scorer in enumerate(scorers, 1):
       print(f"{i}. {scorer['PLAYER_NAME']} ({scorer['TEAM']}) - {scorer['PREDICTED_PPG']:.1f} PPG")










   print("\n🎯 Top 5 Assist Leaders:")
   assists = get_top_assists(5)
   for i, assist in enumerate(assists, 1):
       print(f"{i}. {assist['PLAYER_NAME']} ({assist['TEAM']}) - {assist['PREDICTED_APG']:.1f} APG")












   print("\n🏀 Top 5 Rebounders:")
   rebounders = get_top_rebounders(5)
   for i, rebounder in enumerate(rebounders, 1):
       print(f"{i}. {rebounder['PLAYER_NAME']} ({rebounder['TEAM']}) - {rebounder['PREDICTED_RPG']:.1f} RPG")


















   print("\n=== BREAKOUT PLAYERS ===")
   breakouts = get_breakout_players(5, threshold=3.0)
   for i, breakout in enumerate(breakouts, 1):
       print(f"{i}. {breakout['PLAYER_NAME']} ({breakout['TEAM']}) - {breakout['TOTAL_IMPROVEMENT']:.1f}% improvement")























































