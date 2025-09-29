#!/usr/bin/env python3
"""
Demo script for the NBA PyTorch AI Predictor
This script demonstrates the complete workflow from data collection to predictions
"""

import os
import sys
import time
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🏀 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n📊 {title}")
    print("-" * 40)

def demo_data_collection():
    """Demonstrate data collection"""
    print_section("Data Collection Demo")
    
    try:
        from nba_data_collector import NBADataCollector
        
        collector = NBADataCollector()
        
        # Check if data already exists
        data = collector.load_data()
        if data:
            print(f"✅ Found existing data for {len(data)} players")
            return True
        
        print("🔄 Collecting fresh NBA data...")
        print("Note: This may take several minutes due to API rate limits")
        
        # Collect data for a smaller sample for demo
        data = collector.collect_all_data(max_players=50)
        
        if data:
            collector.save_data(data)
            print(f"✅ Successfully collected data for {len(data)} players")
            return True
        else:
            print("❌ Failed to collect data")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements_pytorch.txt")
        return False
    except Exception as e:
        print(f"❌ Error during data collection: {e}")
        return False

def demo_model_training():
    """Demonstrate model training"""
    print_section("Model Training Demo")
    
    try:
        from nba_ai_predictor import NBAAIPredictor
        
        predictor = NBAAIPredictor()
        
        # Check if model already exists
        model_file = os.path.join(os.path.dirname(__file__), 'nba_model.pkl')
        if os.path.exists(model_file):
            print("✅ Found existing trained model")
            return True
        
        print("🔄 Training PyTorch model...")
        print("This may take a few minutes...")
        
        success = predictor.collect_and_train(max_players=50, force_retrain=False)
        
        if success:
            print("✅ Model training completed successfully!")
            return True
        else:
            print("❌ Model training failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during model training: {e}")
        return False

def demo_predictions():
    """Demonstrate predictions"""
    print_section("AI Predictions Demo")
    
    try:
        from nba_ai_predictor import NBAAIPredictor
        
        predictor = NBAAIPredictor()
        
        # Load model
        if not predictor.analyzer.load_model():
            print("❌ No trained model found. Please train the model first.")
            return False
        
        print("🎯 Getting top performers predictions...")
        top_performers = predictor.get_top_performers(top_n=5)
        
        print("\n🏆 Top 5 Predicted Scorers (PPG):")
        for scorer in top_performers['PPG']:
            print(f"  {scorer['rank']}. {scorer['name']} ({scorer['team']}) - {scorer['predicted_value']:.1f} PPG")
        
        print("\n🎯 Top 5 Predicted Assist Leaders (APG):")
        for assist in top_performers['APG']:
            print(f"  {assist['rank']}. {assist['name']} ({assist['team']}) - {assist['predicted_value']:.1f} APG")
        
        print("\n🏀 Top 5 Predicted Rebounders (RPG):")
        for rebounder in top_performers['RPG']:
            print(f"  {rebounder['rank']}. {rebounder['name']} ({rebounder['team']}) - {rebounder['predicted_value']:.1f} RPG")
        
        print("\n🚀 Top 5 Breakout Players (Predicted Overperformers):")
        breakouts = predictor.get_overperformers(threshold=3.0, top_n=5)
        for breakout in breakouts:
            print(f"  {breakout['rank']}. {breakout['name']} ({breakout['team']}) - {breakout['total_improvement']:.1f}% improvement")
            print(f"     PPG: {breakout['current_ppg']:.1f} → {breakout['predicted_ppg']:.1f} ({breakout['ppg_improvement']:+.1f}%)")
            print(f"     APG: {breakout['current_apg']:.1f} → {breakout['predicted_apg']:.1f} ({breakout['apg_improvement']:+.1f}%)")
            print(f"     RPG: {breakout['current_rpg']:.1f} → {breakout['predicted_rpg']:.1f} ({breakout['rpg_improvement']:+.1f}%)")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error during predictions: {e}")
        return False

def demo_integration():
    """Demonstrate integration with existing backend"""
    print_section("Backend Integration Demo")
    
    try:
        from main import get_ai_predictions, get_ai_player_prediction
        
        print("🔄 Testing AI predictions integration...")
        
        # Test general predictions
        predictions = get_ai_predictions()
        
        if 'error' in predictions:
            print(f"❌ AI Error: {predictions['error']}")
            return False
        
        print("✅ AI predictions integration working!")
        print(f"   - Top scorers: {len(predictions['top_scorers'])} players")
        print(f"   - Top assists: {len(predictions['top_assists'])} players")
        print(f"   - Top rebounders: {len(predictions['top_rebounders'])} players")
        print(f"   - Breakout players: {len(predictions['breakout_players'])} players")
        
        # Test individual player prediction
        if predictions['top_scorers']:
            test_player = predictions['top_scorers'][0]['name']
            print(f"\n🔍 Testing individual prediction for: {test_player}")
            
            player_pred = get_ai_player_prediction(test_player)
            if 'error' not in player_pred:
                print(f"✅ Player prediction working for {test_player}")
            else:
                print(f"❌ Player prediction error: {player_pred['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during integration test: {e}")
        return False

def demo_simple_api():
    """Demonstrate the simple API"""
    print_section("Simple API Demo")
    
    try:
        from ai_predictions import get_top_scorers, get_breakout_players
        
        print("🔄 Testing simple API...")
        
        # Test top scorers
        scorers = get_top_scorers(3)
        if scorers:
            print("✅ Top scorers API working!")
            for scorer in scorers:
                print(f"   {scorer['name']} - {scorer['predicted_value']} PPG")
        
        # Test breakout players
        breakouts = get_breakout_players(3)
        if breakouts:
            print("✅ Breakout players API working!")
            for breakout in breakouts:
                print(f"   {breakout['name']} - {breakout['total_improvement']}% improvement")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during simple API test: {e}")
        return False

def main():
    """Main demo function"""
    print_header("NBA PyTorch AI Predictor - Complete Demo")
    
    print("This demo will show you how to:")
    print("1. Collect NBA player data")
    print("2. Train a PyTorch model")
    print("3. Make performance predictions")
    print("4. Integrate with your existing backend")
    print("5. Use the simple API")
    
    input("\nPress Enter to start the demo...")
    
    # Step 1: Data Collection
    print_header("Step 1: Data Collection")
    data_success = demo_data_collection()
    
    if not data_success:
        print("\n❌ Demo stopped due to data collection failure.")
        print("Please check your internet connection and NBA API access.")
        return
    
    # Step 2: Model Training
    print_header("Step 2: Model Training")
    model_success = demo_model_training()
    
    if not model_success:
        print("\n❌ Demo stopped due to model training failure.")
        return
    
    # Step 3: Predictions
    print_header("Step 3: AI Predictions")
    pred_success = demo_predictions()
    
    if not pred_success:
        print("\n❌ Demo stopped due to prediction failure.")
        return
    
    # Step 4: Integration
    print_header("Step 4: Backend Integration")
    integration_success = demo_integration()
    
    # Step 5: Simple API
    print_header("Step 5: Simple API")
    api_success = demo_simple_api()
    
    # Summary
    print_header("Demo Summary")
    
    results = {
        "Data Collection": "✅ Success" if data_success else "❌ Failed",
        "Model Training": "✅ Success" if model_success else "❌ Failed",
        "AI Predictions": "✅ Success" if pred_success else "❌ Failed",
        "Backend Integration": "✅ Success" if integration_success else "❌ Failed",
        "Simple API": "✅ Success" if api_success else "❌ Failed"
    }
    
    for step, result in results.items():
        print(f"{step:20} : {result}")
    
    if all([data_success, model_success, pred_success]):
        print("\n🎉 Demo completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python nba_ai_predictor.py --menu' for interactive mode")
        print("2. Integrate AI predictions into your web frontend")
        print("3. Customize the model for your specific needs")
        print("4. Add more features and improve predictions")
    else:
        print("\n⚠️  Demo completed with some issues.")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()
