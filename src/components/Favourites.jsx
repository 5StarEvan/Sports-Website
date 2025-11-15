import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getFavorites, removeFavorite } from '../utils/favorites';
import './Stats.css';

const Favourites = () => {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFavorites();
  }, []);

  const loadFavorites = () => {
    try {
      const favList = getFavorites();
      setFavorites(favList);
    } catch (error) {
      console.error('Error loading favorites:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveFavorite = (playerId) => {
    removeFavorite(playerId);
    loadFavorites(); // Reload after removal
  };

  if (loading) {
    return (
      <div className="stats-container">
        <div className="loading">Loading favorites...</div>
      </div>
    );
  }

  return (
    <div className="stats-container">
      <div className="stats-header">
        <Link to="/" className="back-to-home">← Back to Home</Link>
        <h1>⭐ Favourites</h1>
        <p>Your favorite NBA players ({favorites.length})</p>
      </div>

      {favorites.length === 0 ? (
        <div style={{ 
          textAlign: 'center', 
          padding: '60px 20px', 
          color: 'rgba(255, 255, 255, 0.8)',
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '15px',
          backdropFilter: 'blur(10px)',
          maxWidth: '600px',
          margin: '0 auto'
        }}>
          <div style={{ fontSize: '4rem', marginBottom: '20px' }}>⭐</div>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '10px', color: '#ffd700' }}>
            No favorites yet
          </h2>
          <p style={{ fontSize: '1.1rem', marginBottom: '20px' }}>
            Go to the Stats page and click the star icon to favorite players!
          </p>
          <Link 
            to="/stats" 
            style={{
              display: 'inline-block',
              padding: '12px 30px',
              background: 'linear-gradient(45deg, #ffd700, #ffed4e)',
              color: '#333',
              textDecoration: 'none',
              borderRadius: '10px',
              fontWeight: 'bold',
              transition: 'transform 0.3s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
          >
            Go to Stats →
          </Link>
        </div>
      ) : (
        <>
          {/* View Mode Toggle */}
          <div className="controls-section">
            <div style={{ textAlign: 'center', width: '100%' }}>
              <p style={{ opacity: 0.9, fontSize: '1rem' }}>
                Click the ⭐ icon to remove a player from favorites
              </p>
            </div>
          </div>

          {/* Favorites Grid */}
          <div className="players-grid">
            {favorites.map(player => (
              <div key={player.id} className="player-card">
                <div className="player-header">
                  <div className="player-header-top">
                    <h3 className="player-name">{player.name}</h3>
                    <button
                      className="favorite-btn-card favorited"
                      onClick={() => handleRemoveFavorite(player.id)}
                      title="Remove from favorites"
                    >
                      ⭐
                    </button>
                  </div>
                  <div className="player-team-position">
                    <span className="team-badge">{player.team}</span>
                    <span className="position-badge">{player.position}</span>
                  </div>
                </div>
                
                <div className="player-info">
                  <div className="player-details">
                    <span>Age: {player.age}</span>
                    {player.height && (
                      <span>Height: {Math.floor(player.height / 12)}'{player.height % 12}"</span>
                    )}
                    {player.weight && (
                      <span>Weight: {player.weight} lbs</span>
                    )}
                  </div>
                </div>

                {player.stats && (
                  <div className="player-stats">
                    <h4>Current Season Stats</h4>
                    <div className="stats-grid">
                      <div className="stat-item">
                        <span className="stat-label">PPG</span>
                        <span className="stat-value">{player.stats?.ppg_last?.toFixed(1) || '0.0'}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">APG</span>
                        <span className="stat-value">{player.stats?.apg_last?.toFixed(1) || '0.0'}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">RPG</span>
                        <span className="stat-value">{player.stats?.rpg_last?.toFixed(1) || '0.0'}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">SPG</span>
                        <span className="stat-value">{player.stats?.spg_last?.toFixed(1) || '0.0'}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">BPG</span>
                        <span className="stat-value">{player.stats?.bpg_last?.toFixed(1) || '0.0'}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">FG%</span>
                        <span className="stat-value">{player.stats?.fg_pct_last?.toFixed(1) || '0.0'}%</span>
                      </div>
                      {player.stats?.fg3_pct_last && (
                        <div className="stat-item">
                          <span className="stat-label">3P%</span>
                          <span className="stat-value">{player.stats.fg3_pct_last.toFixed(1)}%</span>
                        </div>
                      )}
                      {player.stats?.ft_pct_last && (
                        <div className="stat-item">
                          <span className="stat-label">FT%</span>
                          <span className="stat-value">{player.stats.ft_pct_last.toFixed(1)}%</span>
                        </div>
                      )}
                      {player.stats?.games_played && (
                        <div className="stat-item">
                          <span className="stat-label">Games</span>
                          <span className="stat-value">{player.stats.games_played}</span>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {player.trends && (
                  <div className="player-trends">
                    <h4>Performance Trends</h4>
                    <div className="trends-grid">
                      {player.trends.consistency_score && (
                        <div className="trend-item">
                          <span className="trend-label">Consistency</span>
                          <span className="trend-value">{player.trends.consistency_score.toFixed(2)}</span>
                        </div>
                      )}
                      {player.trends.ppg_trend !== undefined && (
                        <div className="trend-item">
                          <span className="trend-label">PPG Trend</span>
                          <span className={`trend-value ${(player.trends.ppg_trend || 0) > 0 ? 'positive' : 'negative'}`}>
                            {(player.trends.ppg_trend || 0) > 0 ? '+' : ''}{player.trends.ppg_trend.toFixed(1)}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default Favourites;
