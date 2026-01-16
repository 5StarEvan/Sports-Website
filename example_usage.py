import main
import PlayerPerformancePredictor

def test_player_performance_prediction():
    """Example of how to use the PlayerPerformancePredictor with your existing code"""
    
    # Initialize the predictor
    predictor = PlayerPerformancePredictor.PlayerPerformancePredictor()
    
    # Load or train the model
    if not predictor.load_model():
        print("Training new model...")
        predictor.train_model()
    
    # Get your favorite players from the existing code
    favourite_players = main.read_favourite_players()
    player_objects = []
    
    for player_name in favourite_players:
        player_obj = main.get_player_stats(player_name)
        if player_obj:
            player_objects.append(player_obj)
    
    # Example opponent teams
    opponent_teams = [
        "Los Angeles Lakers",
        "Boston Celtics", 
        "Golden State Warriors",
        "Miami Heat",
        "Dallas Mavericks"
    ]
    
    print("=" * 80)
    print("NBA PLAYER PERFORMANCE PREDICTIONS")
    print("=" * 80)
    
    # Test predictions for each player against different teams
    for player_obj in player_objects:
        print(f"\nAnalyzing {player_obj.name}...")
        
        for opponent_team in opponent_teams[:2]:  # Test against first 2 teams
            # Get detailed analysis
            analysis = predictor.analyze_player_performance(player_obj, opponent_team)
            
            # Print the analysis
            predictor.print_analysis(analysis)
    
    # Example of getting just a rating
    if player_objects:
        player = player_objects[0]
        opponent = "Los Angeles Lakers"
        rating = predictor.predict_performance_rating(player, opponent)
        print(f"\nQuick Rating: {player.name} vs {opponent}: {rating}/10")

if __name__ == "__main__":
    test_player_performance_prediction() 