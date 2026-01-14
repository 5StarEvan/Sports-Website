import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './TrendingNow.css';

const TrendingNow = () => {
  const [trendingPlayers, setTrendingPlayers] = useState([]);
  const [upcomingGames, setUpcomingGames] = useState([]);
  const [liveGames, setLiveGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('players'); // 'players', 'upcoming', 'live'

  const API_BASE_URL = '/api';

  useEffect(() => {
    fetchTrendingData();
    // Refresh every 5 minutes
    const interval = setInterval(fetchTrendingData, 300000);
    return () => clearInterval(interval);
  }, []);

  const fetchTrendingData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch trending players
      const playersResponse = await fetch(`${API_BASE_URL}/trending/players`);
      if (playersResponse.ok) {
        const playersData = await playersResponse.json();
        const players = playersData.trending_players || [];
        setTrendingPlayers(players);
        console.log(`Loaded ${players.length} trending players (source: ${playersData.source || 'unknown'})`);
        
        if (players.length === 0 && playersData.message) {
          console.warn('No trending players:', playersData.message);
        }
      } else {
        const errorData = await playersResponse.json().catch(() => ({}));
        console.error('Failed to fetch trending players:', errorData.error || playersResponse.statusText);
      }
      
      // Fetch games
      const gamesResponse = await fetch(`${API_BASE_URL}/trending/games`);
      if (gamesResponse.ok) {
        const gamesData = await gamesResponse.json();
        setUpcomingGames(gamesData.upcoming_games || []);
        setLiveGames(gamesData.live_games || []);
        console.log(`Loaded ${gamesData.upcoming_games?.length || 0} upcoming and ${gamesData.live_games?.length || 0} live games`);
      } else {
        const errorData = await gamesResponse.json().catch(() => ({}));
        console.error('Failed to fetch games:', errorData.error || gamesResponse.statusText);
      }
      
    } catch (err) {
      setError(err.message);
      console.error('Failed to fetch trending data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && trendingPlayers.length === 0) {
    return (
      <div className="trending-container">
        <div className="loading">Loading trending data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="trending-container">
        <div className="error">
          Error: {error}
          <br />
          <button onClick={fetchTrendingData}>Retry</button>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'players', label: 'Trending Players', count: trendingPlayers.length },
    { id: 'upcoming', label: 'Upcoming Games', count: upcomingGames.length },
    { id: 'live', label: 'Live Games', count: liveGames.length }
  ];

  return (
    <div className="trending-container">
      <div className="trending-header">
        <Link to="/" className="back-to-home">← Back to Home</Link>
        <h1>🔥 Trending Now</h1>
        <p>Real-time NBA performance and game updates</p>
      </div>

      <div className="trending-tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label} {tab.count > 0 && <span className="badge">{tab.count}</span>}
          </button>
        ))}
      </div>

      <div className="trending-content">
        {activeTab === 'players' && (
          <div className="trending-players">
            <h2>🔥 Hot Players (Last 7 Days)</h2>
            {trendingPlayers.length > 0 ? (
              <div className="players-grid">
                {trendingPlayers.map((player, index) => (
                  <div key={index} className="trending-player-card">
                    <div className="player-rank">#{index + 1}</div>
                    <div className="player-info">
                      <div className="player-name">{player.name}</div>
                      <div className="player-team">{player.team}</div>
                    </div>
                    <div className="player-stats">
                      <div className="stat">
                        <span className="stat-value">{player.ppg}</span>
                        <span className="stat-label">PPG</span>
                      </div>
                      <div className="stat">
                        <span className="stat-value">{player.apg}</span>
                        <span className="stat-label">APG</span>
                      </div>
                      <div className="stat">
                        <span className="stat-value">{player.rpg}</span>
                        <span className="stat-label">RPG</span>
                      </div>
                    </div>
                    <div className={`trend-indicator ${player.trend}`}>
                      {player.trend === 'up' ? '📈' : player.trend === 'down' ? '📉' : '➡️'}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No trending players data available</div>
            )}
          </div>
        )}

        {activeTab === 'upcoming' && (
          <div className="upcoming-games">
            <h2>📅 Upcoming Games</h2>
            {upcomingGames.length > 0 ? (
              <div className="games-list">
                {upcomingGames.map((game, index) => (
                  <div key={index} className="game-card">
                    <div className="game-teams">
                      <div className="team">
                        <span className="team-name">{game.away_team || 'TBD'}</span>
                      </div>
                      <div className="vs">@</div>
                      <div className="team">
                        <span className="team-name">{game.home_team || 'TBD'}</span>
                      </div>
                    </div>
                    <div className="game-time">{game.time || 'TBD'}</div>
                    <div className="game-status">{game.status || 'Scheduled'}</div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No upcoming games scheduled</div>
            )}
          </div>
        )}

        {activeTab === 'live' && (
          <div className="live-games">
            <h2>⚡ Live Games</h2>
            {liveGames.length > 0 ? (
              <div className="games-list">
                {liveGames.map((game, index) => (
                  <div key={index} className="game-card live">
                    <div className="live-indicator">🔴 LIVE</div>
                    <div className="game-teams">
                      <div className="team">
                        <span className="team-name">{game.away_team || 'TBD'}</span>
                        <span className="team-score">{game.away_score || 0}</span>
                      </div>
                      <div className="vs">@</div>
                      <div className="team">
                        <span className="team-name">{game.home_team || 'TBD'}</span>
                        <span className="team-score">{game.home_score || 0}</span>
                      </div>
                    </div>
                    <div className="game-time">{game.time_remaining || 'Q4'}</div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No live games at the moment</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TrendingNow;
