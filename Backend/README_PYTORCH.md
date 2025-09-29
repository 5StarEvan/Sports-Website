# NBA AI Predictor - PyTorch Model

This module provides a comprehensive PyTorch-based machine learning system for predicting NBA player performance and identifying breakout candidates.

## Features

- **Data Collection**: Automated collection of NBA player statistics from the past 2 years
- **PyTorch Model**: Deep neural network for performance prediction
- **Top Performers**: Predicts players with highest PPG, APG, and RPG
- **Breakout Detection**: Identifies players likely to overperform compared to last season
- **Player Analysis**: Individual player performance predictions

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements_pytorch.txt
```

2. The system uses the existing `nba_api` library which is already installed in your environment.

## Quick Start

### 1. Collect Data and Train Model

```python
from nba_ai_predictor import NBAAIPredictor

predictor = NBAAIPredictor()
predictor.collect_and_train(max_players=150)
```

### 2. Get Predictions

```python
# Get top performers
top_performers = predictor.get_top_performers(top_n=10)

# Find breakout players
breakout_players = predictor.get_overperformers(threshold=5.0, top_n=15)

# Get specific player prediction
player_prediction = predictor.get_player_prediction("LeBron James")
```

### 3. Interactive Mode

```bash
python nba_ai_predictor.py --menu
```

## File Structure

- `nba_data_collector.py` - Data collection and preprocessing
- `nba_pytorch_model.py` - PyTorch model implementation
- `nba_ai_predictor.py` - Main integration and interface
- `ai_predictions.py` - Simple API for web integration
- `requirements_pytorch.txt` - Additional dependencies

## Model Architecture

The PyTorch model uses a multi-layer perceptron with:
- **Input Layer**: 35+ features (player stats, trends, consistency metrics)
- **Hidden Layers**: 256 → 128 → 64 neurons
- **Batch Normalization**: For stable training
- **Dropout**: 30% dropout for regularization
- **Output Layer**: 3 predictions (PPG, APG, RPG)

## Features Used

### Basic Player Info
- Height, Weight, Age, Position, Team

### Current Season Stats
- PPG, APG, RPG, SPG, BPG, TOV
- Field Goal %, 3-Point %, Free Throw %
- Minutes per game, Games played

### Previous Season Stats
- All the above metrics from previous season

### Advanced Metrics
- Last 10 games averages
- Performance trends (improvement/decline)
- Consistency scores (standard deviation)
- Rolling averages

## Usage Examples

### Basic Usage

```python
from ai_predictions import get_top_scorers, get_breakout_players

# Get top 10 predicted scorers
scorers = get_top_scorers(10)
for scorer in scorers:
    print(f"{scorer['name']} - {scorer['predicted_value']} PPG")

# Get breakout players
breakouts = get_breakout_players(10)
for breakout in breakouts:
    print(f"{breakout['name']} - {breakout['total_improvement']}% improvement")
```

### Integration with Existing Backend

```python
from main import get_ai_predictions, get_ai_player_prediction

# Get all AI predictions
predictions = get_ai_predictions()

# Get specific player prediction
player_pred = get_ai_player_prediction("Stephen Curry")
```

### Command Line Usage

```bash
# Quick demo
python nba_ai_predictor.py

# Interactive menu
python nba_ai_predictor.py --menu

# Test predictions
python ai_predictions.py
```

## Data Sources

The system uses the official NBA API (`nba_api` library) to collect:
- Player career statistics
- Game-by-game logs
- Player information (height, weight, age, etc.)
- Team affiliations

## Model Training

The model is trained on:
- **Input**: Player features from past seasons
- **Target**: Next season performance (simulated for demo)
- **Validation**: 20% split for model evaluation
- **Optimization**: Adam optimizer with learning rate scheduling

## Performance Metrics

The model tracks:
- Mean Squared Error (MSE)
- Mean Absolute Error (MAE)
- R² Score
- Training/Validation loss curves

## Customization

### Adjusting Model Architecture

```python
# In nba_pytorch_model.py
model = NBAPerformancePredictor(
    input_size=50,
    hidden_sizes=[512, 256, 128, 64],  # Custom architecture
    dropout_rate=0.2  # Custom dropout
)
```

### Changing Prediction Thresholds

```python
# Find players with >10% improvement
overperformers = predictor.get_overperformers(threshold=10.0)
```

### Adding New Features

Modify the `calculate_player_features` method in `nba_data_collector.py` to add new statistical features.

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements_pytorch.txt
   ```

2. **No Data**: Run data collection first
   ```python
   predictor.collect_and_train()
   ```

3. **Model Not Found**: Train the model first
   ```python
   predictor.collect_and_train()
   ```

4. **Rate Limiting**: The NBA API has rate limits. The system includes delays, but you may need to reduce `max_players` if you encounter issues.

### Performance Tips

- Start with fewer players (50-100) for faster training
- Use GPU if available (automatically detected)
- Adjust batch size based on available memory

## Future Enhancements

Potential improvements:
- Real-time data updates
- More sophisticated feature engineering
- Ensemble models
- Player similarity analysis
- Injury prediction
- Team chemistry factors

## API Reference

### NBAAIPredictor Class

- `collect_and_train(max_players=150, force_retrain=False)`
- `get_top_performers(top_n=10)`
- `get_overperformers(threshold=5.0, top_n=15)`
- `get_player_prediction(player_name)`
- `generate_report(output_file='nba_predictions_report.json')`

### Convenience Functions

- `get_top_scorers(limit=10)`
- `get_top_assists(limit=10)`
- `get_top_rebounders(limit=10)`
- `get_breakout_players(limit=10)`
- `get_player_outlook(player_name)`
- `get_all_predictions()`

## License

This module is part of the Sports Website project and follows the same licensing terms.
