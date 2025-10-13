import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Stats.css';

const Stats = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTeam, setSelectedTeam] = useState('');
  const [selectedPosition, setSelectedPosition] = useState('');
  const [teams, setTeams] = useState([]);
  const [positions, setPositions] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');

  const API_BASE_URL = 'http://localhost:5000/api';

  useEffect(() => {
    fetchTeams();
    fetchPositions();
    fetchPlayers();
  }, [currentPage, searchTerm, selectedTeam, selectedPosition]);

  const fetchPlayers = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        page: currentPage.toString(),
        limit: '50'  // Show 50 players per page instead of 20
      });
      
      if (searchTerm) params.append('search', searchTerm);
      if (selectedTeam) params.append('team', selectedTeam);
      if (selectedPosition) params.append('position', selectedPosition);

      const response = await fetch(`${API_BASE_URL}/players?${params}`);
      if (!response.ok) throw new Error('Failed to fetch players');
      
      const data = await response.json();
      setPlayers(data.players || []);
      setTotalPages(data.pagination?.total_pages || 1);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchTeams = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/teams`);
      if (response.ok) {
        const data = await response.json();
        setTeams(data.teams || []);
      }
    } catch (err) {
      console.error('Failed to fetch teams:', err);
    }
  };

  const fetchPositions = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/positions`);
      if (response.ok) {
        const data = await response.json();
        setPositions(data.positions || []);
      }
    } catch (err) {
      console.error('Failed to fetch positions:', err);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const handleTeamFilter = (e) => {
    setSelectedTeam(e.target.value);
    setCurrentPage(1);
  };

  const handlePositionFilter = (e) => {
    setSelectedPosition(e.target.value);
    setCurrentPage(1);
  };

  const clearFilters = () => {
    setSearchTerm('');
    setSelectedTeam('');
    setSelectedPosition('');
    setCurrentPage(1);
  };

  const sortedPlayers = [...players].sort((a, b) => {
    let aValue, bValue;
    
    switch (sortBy) {
      case 'name':
        aValue = a.name;
        bValue = b.name;
        break;
      case 'ppg':
        aValue = a.stats.ppg_last;
        bValue = b.stats.ppg_last;
        break;
      case 'apg':
        aValue = a.stats.apg_last;
        bValue = b.stats.apg_last;
        break;
      case 'rpg':
        aValue = a.stats.rpg_last;
        bValue = b.stats.rpg_last;
        break;
      default:
        aValue = a.name;
        bValue = b.name;
    }
    
    if (sortOrder === 'asc') {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });

  const handleSort = (newSortBy) => {
    if (sortBy === newSortBy) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(newSortBy);
      setSortOrder('asc');
    }
  };

  if (loading && players.length === 0) {
    return (
      <div className="stats-container">
        <div className="loading">Loading NBA players...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="stats-container">
        <div className="error">
          Error: {error}
          <br />
          Make sure the Flask API server is running on http://localhost:5000
        </div>
      </div>
    );
  }

  return (
    <div className="stats-container">
      <div className="stats-header">
        <Link to="/" className="back-to-home">← Back to Home</Link>
        <h1>🏀 NBA Player Statistics</h1>
        <p>Browse and analyze NBA player performance data</p>
      </div>

      {/* Filters */}
      <div className="filters-section">
        <div className="filter-group">
          <input
            type="text"
            placeholder="Search players..."
            value={searchTerm}
            onChange={handleSearch}
            className="search-input"
          />
        </div>
        
        <div className="filter-group">
          <select value={selectedTeam} onChange={handleTeamFilter} className="filter-select">
            <option value="">All Teams</option>
            {teams.map(team => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <select value={selectedPosition} onChange={handlePositionFilter} className="filter-select">
            <option value="">All Positions</option>
            {positions.map(position => (
              <option key={position} value={position}>{position}</option>
            ))}
          </select>
        </div>
        
        <button onClick={clearFilters} className="clear-filters-btn">
          Clear Filters
        </button>
      </div>

      {/* Sorting */}
      <div className="sorting-section">
        <span>Sort by:</span>
        <button 
          className={`sort-btn ${sortBy === 'name' ? 'active' : ''}`}
          onClick={() => handleSort('name')}
        >
          Name {sortBy === 'name' && (sortOrder === 'asc' ? '↑' : '↓')}
        </button>
        <button 
          className={`sort-btn ${sortBy === 'ppg' ? 'active' : ''}`}
          onClick={() => handleSort('ppg')}
        >
          PPG {sortBy === 'ppg' && (sortOrder === 'asc' ? '↑' : '↓')}
        </button>
        <button 
          className={`sort-btn ${sortBy === 'apg' ? 'active' : ''}`}
          onClick={() => handleSort('apg')}
        >
          APG {sortBy === 'apg' && (sortOrder === 'asc' ? '↑' : '↓')}
        </button>
        <button 
          className={`sort-btn ${sortBy === 'rpg' ? 'active' : ''}`}
          onClick={() => handleSort('rpg')}
        >
          RPG {sortBy === 'rpg' && (sortOrder === 'asc' ? '↑' : '↓')}
        </button>
      </div>

      {/* Players Grid */}
      <div className="players-grid">
        {sortedPlayers.map(player => (
          <div key={player.id} className="player-card">
            <div className="player-header">
              <h3 className="player-name">{player.name}</h3>
              <div className="player-team-position">
                <span className="team-badge">{player.team}</span>
                <span className="position-badge">{player.position}</span>
              </div>
            </div>
            
            <div className="player-info">
              <div className="player-details">
                <span>Age: {player.age}</span>
                <span>Height: {Math.floor(player.height / 12)}'{player.height % 12}"</span>
                <span>Weight: {player.weight} lbs</span>
              </div>
            </div>

            <div className="player-stats">
              <h4>Current Season Stats</h4>
              <div className="stats-grid">
                <div className="stat-item">
                  <span className="stat-label">PPG</span>
                  <span className="stat-value">{player.stats.ppg_last}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">APG</span>
                  <span className="stat-value">{player.stats.apg_last}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">RPG</span>
                  <span className="stat-value">{player.stats.rpg_last}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">SPG</span>
                  <span className="stat-value">{player.stats.spg_last}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">BPG</span>
                  <span className="stat-value">{player.stats.bpg_last}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">FG%</span>
                  <span className="stat-value">{player.stats.fg_pct_last}%</span>
                </div>
              </div>
            </div>

            <div className="player-trends">
              <h4>Performance Trends</h4>
              <div className="trends-grid">
                <div className="trend-item">
                  <span className="trend-label">Consistency</span>
                  <span className="trend-value">{player.trends.consistency_score}</span>
                </div>
                <div className="trend-item">
                  <span className="trend-label">PPG Trend</span>
                  <span className={`trend-value ${player.trends.ppg_trend > 0 ? 'positive' : 'negative'}`}>
                    {player.trends.ppg_trend > 0 ? '+' : ''}{player.trends.ppg_trend}
                  </span>
                </div>
                <div className="trend-item">
                  <span className="trend-label">Games Played</span>
                  <span className="trend-value">{player.stats.games_played}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Pagination */}
      <div className="pagination">
        <button 
          onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
          disabled={currentPage === 1}
          className="pagination-btn"
        >
          Previous
        </button>
        
        <span className="pagination-info">
          Page {currentPage} of {totalPages}
        </span>
        
        <button 
          onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
          disabled={currentPage === totalPages}
          className="pagination-btn"
        >
          Next
        </button>
      </div>

      {loading && (
        <div className="loading-overlay">
          <div className="loading">Loading more players...</div>
        </div>
      )}
    </div>
  );
};

export default Stats;
