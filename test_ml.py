import main
import PlayerPerformancePredictor

def test_ml_algorithm():
    """Test the ML algorithm with your existing player data"""
    
    # Initialize the predictor
    predictor = PlayerPerformancePredictor.PlayerPerformancePredictor()
    
    # Load or train the model
    if not predictor.load_model():
        print("Training new model...")
        predictor.train_model()
    
    # Get your favorite players
    favourite_players = main.read_favourite_players()
    player_objects = []
    
    for player_name in favourite_players:
        player_obj = main.get_player_stats(player_name)
        if player_obj:
            player_objects.append(player_obj)
    
    # Test predictions against different teams
    test_teams = ["Los Angeles Lakers", "Boston Celtics", "Golden State Warriors", "Miami Heat"]
    
    print("\n" + "="*80)
    print("ML PERFORMANCE PREDICTIONS")
    print("="*80)
    
    for player_obj in player_objects:
        print(f"\nAnalyzing {player_obj.name}:")
        for team in test_teams:
            rating = predictor.predict_performance_rating(player_obj, team)
            print(f"  vs {team}: {rating}/10")
    
    # Detailed analysis for first player
    if player_objects:
        print(f"\n" + "="*80)
        print("DETAILED ANALYSIS")
        print("="*80)
        analysis = predictor.analyze_player_performance(player_objects[0], "Los Angeles Lakers")
        predictor.print_analysis(analysis)

if __name__ == "__main__":
    test_ml_algorithm() 