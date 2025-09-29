import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
import os
from typing import Dict, List, Tuple, Optional

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

class NBAModelTrainer:
    """Trainer class for NBA performance prediction model"""
    
    def __init__(self, model, device='cpu'):
        self.model = model.to(device)
        self.device = device
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.target_columns = ['PPG_NEXT', 'APG_NEXT', 'RPG_NEXT']
        
    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare and preprocess the data for training"""
        
        # Handle missing values
        df = df.fillna(0)
        
        # Encode categorical variables
        categorical_columns = ['POSITION', 'TEAM']
        for col in categorical_columns:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
        
        # Select features for training
        feature_columns = [
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
        
        # Add categorical columns if they exist
        for col in categorical_columns:
            if col in df.columns:
                feature_columns.append(col)
        
        # Filter to only existing columns
        self.feature_columns = [col for col in feature_columns if col in df.columns]
        
        # Create target variables (next season performance)
        # For this example, we'll use current season as "next" season prediction
        # In a real scenario, you'd have actual next season data
        df['PPG_NEXT'] = df['PPG_LAST'] + np.random.normal(0, 0.5, len(df))  # Simulated improvement
        df['APG_NEXT'] = df['APG_LAST'] + np.random.normal(0, 0.3, len(df))
        df['RPG_NEXT'] = df['RPG_LAST'] + np.random.normal(0, 0.4, len(df))
        
        # Prepare features and targets
        X = df[self.feature_columns].values
        y = df[self.target_columns].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y
    
    def train(self, X, y, epochs=100, batch_size=32, learning_rate=0.001, validation_split=0.2):
        """Train the model"""
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, random_state=42
        )
        
        # Create datasets and dataloaders
        train_dataset = NBADataset(X_train, y_train)
        val_dataset = NBADataset(X_val, y_val)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        # Initialize optimizer and loss function
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=1e-5)
        criterion = nn.MSELoss()
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=10, factor=0.5)
        
        # Training loop
        train_losses = []
        val_losses = []
        
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
            
            train_losses.append(train_loss)
            val_losses.append(val_loss)
            
            scheduler.step(val_loss)
            
            if epoch % 10 == 0:
                print(f'Epoch {epoch}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')
        
        return train_losses, val_losses
    
    def predict(self, X):
        """Make predictions"""
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            predictions = self.model(X_tensor)
            return predictions.cpu().numpy()
    
    def save_model(self, filepath):
        """Save the trained model and preprocessing objects"""
        model_data = {
            'model_state_dict': self.model.state_dict(),
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'target_columns': self.target_columns
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a trained model"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model.load_state_dict(model_data['model_state_dict'])
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        self.target_columns = model_data['target_columns']
        
        print(f"Model loaded from {filepath}")

class NBAPerformanceAnalyzer:
    """Main class for NBA performance analysis and predictions"""
    
    def __init__(self):
        self.model = None
        self.trainer = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
    
    def train_model(self, data_file='nba_player_data.pkl', model_file='nba_model.pkl'):
        """Train the NBA performance prediction model"""
        
        # Load data
        data_path = os.path.join(os.path.dirname(__file__), data_file)
        if not os.path.exists(data_path):
            print(f"Data file {data_file} not found. Please run data collection first.")
            return False
        
        with open(data_path, 'rb') as f:
            data = pickle.load(f)
        
        df = pd.DataFrame(data)
        print(f"Loaded data for {len(df)} players")
        
        # Initialize model
        input_size = len(df.columns) - 3  # Approximate, will be adjusted in prepare_data
        self.model = NBAPerformancePredictor(input_size=50)  # Will be adjusted
        self.trainer = NBAModelTrainer(self.model, self.device)
        
        # Prepare data
        X, y = self.trainer.prepare_data(df)
        print(f"Training data shape: {X.shape}, Target shape: {y.shape}")
        
        # Update model input size
        actual_input_size = X.shape[1]
        self.model = NBAPerformancePredictor(input_size=actual_input_size)
        self.trainer = NBAModelTrainer(self.model, self.device)
        
        # Train model
        print("Training model...")
        train_losses, val_losses = self.trainer.train(X, y, epochs=200)
        
        # Save model
        model_path = os.path.join(os.path.dirname(__file__), model_file)
        self.trainer.save_model(model_path)
        
        print("Model training completed!")
        return True
    
    def predict_top_performers(self, data_file='nba_player_data.pkl', model_file='nba_model.pkl', top_n=10):
        """Predict top performers for PPG, APG, and RPG"""
        
        if self.trainer is None:
            self.load_model(model_file)
        
        # Load data
        data_path = os.path.join(os.path.dirname(__file__), data_file)
        with open(data_path, 'rb') as f:
            data = pickle.load(f)
        
        df = pd.DataFrame(data)
        
        # Prepare data for prediction
        df_processed = df.fillna(0)
        
        # Encode categorical variables
        for col, le in self.trainer.label_encoders.items():
            if col in df_processed.columns:
                df_processed[col] = le.transform(df_processed[col].astype(str))
        
        # Select features
        X = df_processed[self.trainer.feature_columns].values
        X_scaled = self.trainer.scaler.transform(X)
        
        # Make predictions
        predictions = self.trainer.predict(X_scaled)
        
        # Create results DataFrame
        results = df[['PLAYER_NAME', 'TEAM', 'POSITION', 'AGE']].copy()
        results['PREDICTED_PPG'] = predictions[:, 0]
        results['PREDICTED_APG'] = predictions[:, 1]
        results['PREDICTED_RPG'] = predictions[:, 2]
        
        # Get top performers for each stat
        top_performers = {
            'PPG': results.nlargest(top_n, 'PREDICTED_PPG'),
            'APG': results.nlargest(top_n, 'PREDICTED_APG'),
            'RPG': results.nlargest(top_n, 'PREDICTED_RPG')
        }
        
        return top_performers
    
    def find_overperformers(self, data_file='nba_player_data.pkl', model_file='nba_model.pkl', threshold=0.1):
        """Find players who are predicted to overperform compared to last season"""
        
        if self.trainer is None:
            self.load_model(model_file)
        
        # Load data
        data_path = os.path.join(os.path.dirname(__file__), data_file)
        with open(data_path, 'rb') as f:
            data = pickle.load(f)
        
        df = pd.DataFrame(data)
        
        # Prepare data for prediction
        df_processed = df.fillna(0)
        
        # Encode categorical variables
        for col, le in self.trainer.label_encoders.items():
            if col in df_processed.columns:
                df_processed[col] = le.transform(df_processed[col].astype(str))
        
        # Select features
        X = df_processed[self.trainer.feature_columns].values
        X_scaled = self.trainer.scaler.transform(X)
        
        # Make predictions
        predictions = self.trainer.predict(X_scaled)
        
        # Calculate improvement
        results = df[['PLAYER_NAME', 'TEAM', 'POSITION', 'PPG_LAST', 'APG_LAST', 'RPG_LAST']].copy()
        results['PREDICTED_PPG'] = predictions[:, 0]
        results['PREDICTED_APG'] = predictions[:, 1]
        results['PREDICTED_RPG'] = predictions[:, 2]
        
        # Calculate improvement percentages
        results['PPG_IMPROVEMENT'] = (results['PREDICTED_PPG'] - results['PPG_LAST']) / results['PPG_LAST'] * 100
        results['APG_IMPROVEMENT'] = (results['PREDICTED_APG'] - results['APG_LAST']) / results['APG_LAST'] * 100
        results['RPG_IMPROVEMENT'] = (results['PREDICTED_RPG'] - results['RPG_LAST']) / results['RPG_LAST'] * 100
        
        # Find overperformers (improvement > threshold)
        overperformers = results[
            (results['PPG_IMPROVEMENT'] > threshold) |
            (results['APG_IMPROVEMENT'] > threshold) |
            (results['RPG_IMPROVEMENT'] > threshold)
        ].copy()
        
        # Sort by total improvement
        overperformers['TOTAL_IMPROVEMENT'] = (
            overperformers['PPG_IMPROVEMENT'] + 
            overperformers['APG_IMPROVEMENT'] + 
            overperformers['RPG_IMPROVEMENT']
        )
        
        overperformers = overperformers.sort_values('TOTAL_IMPROVEMENT', ascending=False)
        
        return overperformers
    
    def load_model(self, model_file='nba_model.pkl'):
        """Load a trained model"""
        model_path = os.path.join(os.path.dirname(__file__), model_file)
        
        if not os.path.exists(model_path):
            print(f"Model file {model_file} not found. Please train the model first.")
            return False
        
        # Load model data
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        # Initialize model
        input_size = len(model_data['feature_columns'])
        self.model = NBAPerformancePredictor(input_size=input_size)
        self.trainer = NBAModelTrainer(self.model, self.device)
        
        # Load trained weights and preprocessing
        self.trainer.load_model(model_path)
        
        print("Model loaded successfully!")
        return True

if __name__ == "__main__":
    analyzer = NBAPerformanceAnalyzer()
    
    # Train model (uncomment to train)
    # analyzer.train_model()
    
    # Load existing model and make predictions
    if analyzer.load_model():
        print("\n=== TOP PERFORMERS PREDICTION ===")
        top_performers = analyzer.predict_top_performers(top_n=5)
        
        for stat, players in top_performers.items():
            print(f"\nTop 5 {stat} Predictions:")
            for _, player in players.iterrows():
                print(f"{player['PLAYER_NAME']} ({player['TEAM']}) - {player[f'PREDICTED_{stat}']:.2f}")
        
        print("\n=== OVERPERFORMERS ANALYSIS ===")
        overperformers = analyzer.find_overperformers(threshold=5.0)  # 5% improvement threshold
        
        print(f"\nPlayers predicted to overperform (top 10):")
        for _, player in overperformers.head(10).iterrows():
            print(f"{player['PLAYER_NAME']} ({player['TEAM']}) - "
                  f"PPG: {player['PPG_IMPROVEMENT']:.1f}%, "
                  f"APG: {player['APG_IMPROVEMENT']:.1f}%, "
                  f"RPG: {player['RPG_IMPROVEMENT']:.1f}%")
