import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Recommendations.css';

const Recommendations = () => {
  const [selectedCategory, setSelectedCategory] = useState('players');

  const insights = [
    {
      id: 1,
      title: 'Rising Stars Alert',
      category: 'Trending',
      description: 'Young players showing exceptional growth this season with significant stat improvements',
      icon: '📈',
      details: 'Players under 25 averaging 20+ PPG increased by 15% this season',
      link: '/stats'
    },
    {
      id: 2,
      title: 'Defensive Powerhouses',
      category: 'Analysis',
      description: 'Teams with the best defensive ratings and their impact on game outcomes',
      icon: '🛡️',
      details: 'Top 5 defensive teams have 78% win rate in close games',
      link: '/stats'
    },
    {
      id: 3,
      title: 'Three-Point Revolution',
      category: 'Trending',
      description: 'Teams increasing 3-point attempts and their correlation with wins',
      icon: '🎯',
      details: 'Teams shooting 35%+ from 3-point range win 65% more games',
      link: '/stats'
    },
    {
      id: 4,
      title: 'Clutch Performance',
      category: 'Analysis',
      description: 'Players with the best performance in the final 5 minutes of close games',
      icon: '⏰',
      details: 'Top clutch players average 8.5 PPG in final 5 minutes',
      link: '/stats'
    },
    {
      id: 5,
      title: 'Injury Impact Analysis',
      category: 'Insight',
      description: 'How key player injuries affect team performance and betting lines',
      icon: '🏥',
      details: 'Teams missing star players see 12% drop in offensive efficiency',
      link: '/stats'
    },
    {
      id: 6,
      title: 'Home Court Advantage',
      category: 'Analysis',
      description: 'Statistical breakdown of home vs away performance across the league',
      icon: '🏠',
      details: 'Home teams win 58% of games with 4.2 PPG advantage on average',
      link: '/stats'
    }
  ];

  const upcomingGames = [
    {
      id: 1,
      team1: 'Lakers',
      team2: 'Warriors',
      date: 'Tonight 8:00 PM EST',
      prediction: 'Lakers 65%',
      reason: 'Home court advantage and recent form',
      keyMatchup: 'LeBron vs Curry'
    },
    {
      id: 2,
      team1: 'Celtics',
      team2: 'Heat',
      date: 'Tomorrow 7:30 PM EST',
      prediction: 'Celtics 58%',
      reason: 'Strong defensive matchup expected',
      keyMatchup: 'Tatum vs Butler'
    },
    {
      id: 3,
      team1: 'Bucks',
      team2: 'Nuggets',
      date: 'Friday 9:00 PM EST',
      prediction: 'Bucks 52%',
      reason: 'Close matchup, slight edge to home team',
      keyMatchup: 'Giannis vs Jokić'
    }
  ];

  return (
    <div className="recommendations-wrapper">
      <header className="recommendations-header">
        <Link to="/" className="back-link">← Back to Home</Link>
        <h1 className="recommendations-title">
          <span className="title-icon">⭐</span>
          RECOMMENDATIONS
        </h1>
        <p className="recommendations-subtitle">
          AI-powered personalized recommendations based on your preferences
        </p>
      </header>

      <div className="recommendations-content">
        <div className="category-tabs">
          <button
            className={`tab-button ${selectedCategory === 'players' ? 'active' : ''}`}
            onClick={() => setSelectedCategory('players')}
          >
            Insights & Analysis
          </button>
          <button
            className={`tab-button ${selectedCategory === 'games' ? 'active' : ''}`}
            onClick={() => setSelectedCategory('games')}
          >
            Upcoming Games
          </button>
        </div>

        {selectedCategory === 'players' && (
          <div className="recommendations-section">
            <h2 className="section-heading">Basketball Insights & Trends</h2>
            <p className="section-description">
              Discover key insights, trends, and analysis powered by AI to help you understand the game better
            </p>
            <div className="recommendations-grid">
              {insights.map((insight) => (
                <div key={insight.id} className="recommendation-card insight-card">
                  <div className="card-header">
                    <div className="insight-icon">{insight.icon}</div>
                    <div className="category-badge">{insight.category}</div>
                  </div>
                  <div className="card-body">
                    <h3 className="insight-title">{insight.title}</h3>
                    <p className="recommendation-reason">{insight.description}</p>
                    <div className="insight-details">
                      <span className="details-text">{insight.details}</span>
                    </div>
                  </div>
                  <div className="card-footer">
                    <Link to={insight.link} className="view-stats-link">
                      Explore More →
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {selectedCategory === 'games' && (
          <div className="recommendations-section">
            <h2 className="section-heading">Recommended Games to Watch</h2>
            <p className="section-description">
              AI predictions for upcoming games based on team performance and matchups
            </p>
            <div className="games-grid">
              {upcomingGames.map((game) => (
                <div key={game.id} className="game-card">
                  <div className="game-header">
                    <div className="game-teams">
                      <span className="team-name">{game.team1}</span>
                      <span className="vs">VS</span>
                      <span className="team-name">{game.team2}</span>
                    </div>
                    <div className="game-prediction">
                      <span className="prediction-label">AI Prediction</span>
                      <span className="prediction-value">{game.prediction}</span>
                    </div>
                  </div>
                  <div className="game-body">
                    <div className="game-date">{game.date}</div>
                    <div className="game-matchup">
                      <span className="matchup-label">Key Matchup:</span>
                      <span className="matchup-value">{game.keyMatchup}</span>
                    </div>
                    <p className="game-reason">{game.reason}</p>
                  </div>
                  <div className="game-footer">
                    <Link to="/stats" className="view-details-link">
                      View Details →
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Recommendations;
