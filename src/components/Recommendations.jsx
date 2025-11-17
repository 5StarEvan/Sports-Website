import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Recommendations.css';

const Recommendations = () => {
  const [selectedCategory, setSelectedCategory] = useState('players');

  const recommendedPlayers = [
    {
      id: 1,
      name: 'LeBron James',
      team: 'Lakers',
      position: 'SF',
      reason: 'High consistency score and trending upward',
      stats: { ppg: 28.5, apg: 7.2, rpg: 8.1 },
      trend: '+2.3 PPG',
      matchScore: 95
    },
    {
      id: 2,
      name: 'Stephen Curry',
      team: 'Warriors',
      position: 'PG',
      reason: 'Excellent 3-point shooting and recent hot streak',
      stats: { ppg: 30.2, apg: 6.8, rpg: 5.4 },
      trend: '+3.1 PPG',
      matchScore: 92
    },
    {
      id: 3,
      name: 'Giannis Antetokounmpo',
      team: 'Bucks',
      position: 'PF',
      reason: 'Strong all-around performance and defensive impact',
      stats: { ppg: 31.8, apg: 5.7, rpg: 11.2 },
      trend: '+1.8 PPG',
      matchScore: 90
    },
    {
      id: 4,
      name: 'Luka Dončić',
      team: 'Mavericks',
      position: 'PG',
      reason: 'Triple-double threat with high usage rate',
      stats: { ppg: 33.1, apg: 9.2, rpg: 8.7 },
      trend: '+4.2 PPG',
      matchScore: 88
    },
    {
      id: 5,
      name: 'Jayson Tatum',
      team: 'Celtics',
      position: 'SF',
      reason: 'Consistent scoring and improving efficiency',
      stats: { ppg: 27.8, apg: 4.9, rpg: 8.3 },
      trend: '+2.7 PPG',
      matchScore: 87
    },
    {
      id: 6,
      name: 'Nikola Jokić',
      team: 'Nuggets',
      position: 'C',
      reason: 'Elite playmaking center with high assist numbers',
      stats: { ppg: 26.4, apg: 9.8, rpg: 12.1 },
      trend: '+1.5 PPG',
      matchScore: 85
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
            Recommended Players
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
            <h2 className="section-heading">Top Player Recommendations</h2>
            <p className="section-description">
              Based on your viewing history and preferences, here are players you might find interesting
            </p>
            <div className="recommendations-grid">
              {recommendedPlayers.map((player) => (
                <div key={player.id} className="recommendation-card">
                  <div className="card-header">
                    <div className="match-score">
                      <span className="score-number">{player.matchScore}%</span>
                      <span className="score-label">Match</span>
                    </div>
                    <div className="trend-badge positive">
                      {player.trend}
                    </div>
                  </div>
                  <div className="card-body">
                    <h3 className="player-name">{player.name}</h3>
                    <div className="player-meta">
                      <span className="team-badge">{player.team}</span>
                      <span className="position-badge">{player.position}</span>
                    </div>
                    <p className="recommendation-reason">{player.reason}</p>
                    <div className="player-stats-mini">
                      <div className="stat-mini">
                        <span className="stat-label-mini">PPG</span>
                        <span className="stat-value-mini">{player.stats.ppg}</span>
                      </div>
                      <div className="stat-mini">
                        <span className="stat-label-mini">APG</span>
                        <span className="stat-value-mini">{player.stats.apg}</span>
                      </div>
                      <div className="stat-mini">
                        <span className="stat-label-mini">RPG</span>
                        <span className="stat-value-mini">{player.stats.rpg}</span>
                      </div>
                    </div>
                  </div>
                  <div className="card-footer">
                    <Link to="/stats" className="view-stats-link">
                      View Full Stats →
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
