import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Recommendations.css';

const Recommendations = () => {
  const [selectedCategory, setSelectedCategory] = useState('players');

  const insights = [
    {
      id: 1,
      title: 'Rising Stars',
      category: 'Trending',
      description: 'Young players showing exceptional growth this season with significant stat improvements',
      icon: '📈',
      details: 'Biggest predicted PRA jumps for players next season',
      link: '/recommendations/PRA'
    },

    {
      id: 2,
      title: 'Bucket Getters',
      category: 'Trending',
      description: 'Young players showing exceptional growth this season with significant PPG improvements',
      icon: '📈',
      details: 'Biggest predicted PPG jumps for players next season',
      link: '/recommendations/PPG'
    },

    {
      id: 3,
      title: 'Assist Leaders',
      category: 'Trending',
      description: 'Young players showing exceptional growth this season with significant APG improvements',
      icon: '📈',
      details: 'Biggest predicted APG jumps for players next season',
      link: '/recommendations/APG'
    },

    {
      id: 4,
      title: 'Rebound Leaders',
      category: 'Trending',
      description: 'Young players showing exceptional growth this season with significant RPG improvements',
      icon: '📈',
      details: 'Biggest predicted RPG jumps for players next season',
      link: '/recommendations/RPG'
    }
  ]

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
