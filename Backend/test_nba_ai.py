# test_nba_ai_real.py
import sys
import os
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

def test_complete_system():
    """Test the complete NBA AI system with real scraper"""
    print("🏀 Testing Complete NBA AI System with Real Scraper")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Import the system
        from nba_ai_system import NBAAISystem, initialize_nba_ai, get_top_scorers, get_top_assists, get_top_rebounders, get_breakout_players, get_player_prediction
        
        # Test 1: Initialize system
        print("\n1. 🎯 INITIALIZING SYSTEM...")
        print("   This may take a few minutes (scraping + training)...")
        
        success = initialize_nba_ai(force_refresh=True)
        if success:
            print("   ✅ System initialized successfully!")
        else:
            print("   ❌ System initialization failed")
            return False
        
        initialization_time = time.time() - start_time
        print(f"   ⏱️  Initialization took: {initialization_time:.2f} seconds")
        
        # Test 2: Get top performers
        print("\n2. 🏆 TESTING TOP PERFORMERS...")
        
        # Top scorers
        print("\n   📊 Top 5 Scorers:")
        scorers = get_top_scorers(5)
        if scorers:
            for i, scorer in enumerate(scorers, 1):
                print(f"      {i}. {scorer['PLAYER_NAME']} ({scorer['TEAM']}) - {scorer['PREDICTED_PPG']:.1f} PPG")
        else:
            print("      ❌ No scorers data")
        
        # Top assist leaders
        print("\n   🎯 Top 5 Assist Leaders:")
        assists = get_top_assists(5)
        if assists:
            for i, assist in enumerate(assists, 1):
                print(f"      {i}. {assist['PLAYER_NAME']} ({assist['TEAM']}) - {assist['PREDICTED_APG']:.1f} APG")
        else:
            print("      ❌ No assists data")
        
        # Top rebounders
        print("\n   🏀 Top 5 Rebounders:")
        rebounders = get_top_rebounders(5)
        if rebounders:
            for i, rebounder in enumerate(rebounders, 1):
                print(f"      {i}. {rebounder['PLAYER_NAME']} ({rebounder['TEAM']}) - {rebounder['PREDICTED_RPG']:.1f} RPG")
        else:
            print("      ❌ No rebounders data")
        
        # Test 3: Get breakout players
        print("\n3. 📈 TESTING BREAKOUT PLAYERS...")
        breakouts = get_breakout_players(5, threshold=3.0)
        if breakouts:
            print("   Players predicted to improve significantly:")
            for i, breakout in enumerate(breakouts, 1):
                improvement = breakout.get('TOTAL_IMPROVEMENT', 0)
                ppg_imp = breakout.get('PPG_IMPROVEMENT', 0)
                apg_imp = breakout.get('APG_IMPROVEMENT', 0)
                rpg_imp = breakout.get('RPG_IMPROVEMENT', 0)
                
                print(f"      {i}. {breakout['PLAYER_NAME']} ({breakout['TEAM']})")
                print(f"         PPG: {breakout.get('PPG_LAST', 0):.1f} → {breakout.get('PREDICTED_PPG', 0):.1f} ({ppg_imp:+.1f}%)")
                print(f"         APG: {breakout.get('APG_LAST', 0):.1f} → {breakout.get('PREDICTED_APG', 0):.1f} ({apg_imp:+.1f}%)")
                print(f"         RPG: {breakout.get('RPG_LAST', 0):.1f} → {breakout.get('PREDICTED_RPG', 0):.1f} ({rpg_imp:+.1f}%)")
                print(f"         Total Improvement: {improvement:.1f}%")
        else:
            print("   ❌ No breakout players data")
        
        # Test 4: Individual player predictions
        print("\n4. 👤 TESTING INDIVIDUAL PLAYER PREDICTIONS...")
        
        # Test with some known players
        test_players = ["LeBron James", "Stephen Curry", "Giannis Antetokounmpo"]
        
        for player_name in test_players:
            print(f"\n   🔍 Analyzing {player_name}...")
            prediction = get_player_prediction(player_name)
            
            if prediction:
                print(f"      Team: {prediction['team']}")
                print(f"      Position: {prediction['position']}")
                print(f"      Age: {prediction['age']}")
                print(f"      Current Stats: {prediction['current_stats']}")
                print(f"      Predicted Stats: {prediction['predicted_stats']}")
                print(f"      Improvements: {prediction['improvements']}")
            else:
                print(f"      ❌ No prediction available for {player_name}")
        
        # Test 5: System diagnostics
        print("\n5. 📊 SYSTEM DIAGNOSTICS...")
        
        # Check if system has data
        if hasattr(NBAAISystem, 'nba_ai_system'):
            system = NBAAISystem.nba_ai_system
            if system.data:
                print(f"   ✅ Loaded data for {len(system.data)} players")
                
                # Show data sample
                df = pd.DataFrame(system.data)
                print(f"   📈 Data columns: {len(df.columns)}")
                print(f"   🎯 Feature columns used: {len(system.feature_columns)}")
                
                # Show some stats about the data
                if 'PPG_LAST' in df.columns:
                    print(f"   🏀 Average PPG: {df['PPG_LAST'].mean():.1f}")
                if 'APG_LAST' in df.columns:
                    print(f"   🎯 Average APG: {df['APG_LAST'].mean():.1f}")
                if 'RPG_LAST' in df.columns:
                    print(f"   📊 Average RPG: {df['RPG_LAST'].mean():.1f}")
        
        total_time = time.time() - start_time
        print(f"\n⏱️  TOTAL TEST TIME: {total_time:.2f} seconds")
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scraper_only():
    """Test just the scraper component"""
    print("\n" + "=" * 50)
    print("🔍 TESTING SCRAPER COMPONENT ONLY")
    print("=" * 50)
    
    try:
        from nba_web_scraper import NBAWebScraper
        
        scraper = NBAWebScraper()
        
        # Test loading existing data
        print("\n1. Loading existing data...")
        data = scraper.load_data()
        
        if data is None:
            print("   No existing data found. Scraping new data...")
            data = scraper.scrape_player_stats('2024-25')
            
            if data:
                scraper.save_data(data)
                print(f"   ✅ Scraped and saved data for {len(data)} players")
            else:
                print("   ❌ Failed to scrape data")
                return False
        else:
            print(f"   ✅ Loaded existing data for {len(data)} players")
        
        # Show data overview
        df = pd.DataFrame(data)
        print(f"\n2. DATA OVERVIEW:")
        print(f"   Total players: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
        
        print(f"\n3. SAMPLE PLAYERS:")
        for i in range(min(5, len(df))):
            player = df.iloc[i]
            print(f"   {i+1}. {player['PLAYER_NAME']} ({player['TEAM']})")
            if 'PPG_LAST' in df.columns:
                print(f"      PPG: {player.get('PPG_LAST', 0):.1f}, APG: {player.get('APG_LAST', 0):.1f}, RPG: {player.get('RPG_LAST', 0):.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def quick_demo():
    """Run a quick demo of the system"""
    print("\n" + "=" * 50)
    print("🚀 QUICK DEMO MODE")
    print("=" * 50)
    
    try:
        from nba_ai_system import initialize_nba_ai, get_top_scorers, get_player_prediction
        
        print("Initializing system...")
        if initialize_nba_ai(force_refresh=False):  # Don't force refresh for quick demo
            print("✅ System ready!")
            
            # Show top 3 scorers
            print("\n🏆 TOP 3 PREDICTED SCORERS:")
            scorers = get_top_scorers(3)
            for i, scorer in enumerate(scorers, 1):
                print(f"{i}. {scorer['PLAYER_NAME']} - {scorer['PREDICTED_PPG']:.1f} PPG")
            
            # Show prediction for a star player
            print("\n🔮 SAMPLE PREDICTION:")
            prediction = get_player_prediction("LeBron James")
            if prediction:
                print(f"Player: {prediction['name']}")
                print(f"Current: {prediction['current_stats']['ppg']} PPG")
                print(f"Predicted: {prediction['predicted_stats']['ppg']} PPG")
                print(f"Improvement: {prediction['improvements']['ppg']}%")
            
        else:
            print("❌ System initialization failed")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    print("🏀 NBA AI SYSTEM TEST SUITE")
    print("Choose test mode:")
    print("1. Complete System Test (Full scraping + training)")
    print("2. Scraper Test Only")
    print("3. Quick Demo")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_complete_system()
    elif choice == "2":
        test_scraper_only()
    elif choice == "3":
        quick_demo()
    else:
        print("Running complete system test...")
        test_complete_system()