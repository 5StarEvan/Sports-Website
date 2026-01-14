import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { isFavorite, toggleFavorite, getFavorites } from '../utils/favorites';
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
  const [totalPlayers, setTotalPlayers] = useState(0);
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [viewMode, setViewMode] = useState('table'); // 'table' or 'cards'
  const [favorites, setFavorites] = useState(new Set()); // Track favorites for re-renders

  const API_BASE_URL = 'http://localhost:5000/api';

  // Load favorites on mount
  useEffect(() => {
    const loadFavorites = () => {
      const favList = getFavorites();
      setFavorites(new Set(favList.map(f => f.id)));
    };
    loadFavorites();
  }, []);

  const handleFavoriteToggle = (player) => {
    const wasFavorite = isFavorite(player.id);
    toggleFavorite(player);
    // Update local state for immediate UI feedback
    const newFavorites = new Set(favorites);
    if (wasFavorite) {
      newFavorites.delete(player.id);
    } else {
      newFavorites.add(player.id);
    }
    setFavorites(newFavorites);
  };

  useEffect(() => {
    fetchTeams();
    fetchPositions();
    fetchPlayers();
  }, [currentPage, searchTerm, selectedTeam, selectedPosition]);

  const fetchPlayers = async () => {
    try {
      setLoading(true);
      // Use stats/all endpoint to get all players, or players endpoint with higher limit
      const params = new URLSearchParams({
        page: currentPage.toString(),
        limit: '1000'  // Show more players per page to display all
      });
      
      if (searchTerm) params.append('search', searchTerm);
      if (selectedTeam) params.append('team', selectedTeam);
      if (selectedPosition) params.append('position', selectedPosition);

      const response = await fetch(`${API_BASE_URL}/players?${params}`);
      if (!response.ok) throw new Error('Failed to fetch players');
      
      const data = await response.json();
      setPlayers(data.players || []);
      setTotalPages(data.pagination?.total_pages || 1);
      setTotalPlayers(data.pagination?.total || 0);
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
        aValue = a.name?.toLowerCase() || '';
        bValue = b.name?.toLowerCase() || '';
        break;
      case 'team':
        aValue = a.team || '';
        bValue = b.team || '';
        break;
      case 'position':
        aValue = a.position || '';
        bValue = b.position || '';
        break;
      case 'ppg':
        aValue = a.stats?.ppg_last || 0;
        bValue = b.stats?.ppg_last || 0;
        break;
      case 'apg':
        aValue = a.stats?.apg_last || 0;
        bValue = b.stats?.apg_last || 0;
        break;
      case 'rpg':
        aValue = a.stats?.rpg_last || 0;
        bValue = b.stats?.rpg_last || 0;
        break;
      case 'spg':
        aValue = a.stats?.spg_last || 0;
        bValue = b.stats?.spg_last || 0;
        break;
      case 'bpg':
        aValue = a.stats?.bpg_last || 0;
        bValue = b.stats?.bpg_last || 0;
        break;
      case 'fg_pct':
        aValue = a.stats?.fg_pct_last || 0;
        bValue = b.stats?.fg_pct_last || 0;
        break;
      case 'fg3_pct':
        aValue = a.stats?.fg3_pct_last || 0;
        bValue = b.stats?.fg3_pct_last || 0;
        break;
      case 'ft_pct':
        aValue = a.stats?.ft_pct_last || 0;
        bValue = b.stats?.ft_pct_last || 0;
        break;
      case 'games':
        aValue = a.stats?.games_played || 0;
        bValue = b.stats?.games_played || 0;
        break;
      default:
        aValue = a.name?.toLowerCase() || '';
        bValue = b.name?.toLowerCase() || '';
    }
    
    if (typeof aValue === 'string') {
      if (sortOrder === 'asc') {
        return aValue.localeCompare(bValue);
      } else {
        return bValue.localeCompare(aValue);
      }
    } else {
      if (sortOrder === 'asc') {
        return aValue - bValue;
      } else {
        return bValue - aValue;
      }
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

      {/* View Mode and Sorting */}
      <div className="controls-section">
        <div className="view-mode-toggle">
          <button 
            className={`view-btn ${viewMode === 'table' ? 'active' : ''}`}
            onClick={() => setViewMode('table')}
          >
            📊 Table View
          </button>
          <button 
            className={`view-btn ${viewMode === 'cards' ? 'active' : ''}`}
            onClick={() => setViewMode('cards')}
          >
            🃏 Card View
          </button>
        </div>
        
        <div className="sorting-section">
          <span className="sort-label">Sort by:</span>
          <button 
            className={`sort-btn ${sortBy === 'name' ? 'active' : ''}`}
            onClick={() => handleSort('name')}
          >
            Name {sortBy === 'name' && (sortOrder === 'asc' ? '↑' : '↓')}
          </button>
          <button 
            className={`sort-btn ${sortBy === 'team' ? 'active' : ''}`}
            onClick={() => handleSort('team')}
          >
            Team {sortBy === 'team' && (sortOrder === 'asc' ? '↑' : '↓')}
          </button>
          <button 
            className={`sort-btn ${sortBy === 'position' ? 'active' : ''}`}
            onClick={() => handleSort('position')}
          >
            Position {sortBy === 'position' && (sortOrder === 'asc' ? '↑' : '↓')}
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
          <button 
            className={`sort-btn ${sortBy === 'fg_pct' ? 'active' : ''}`}
            onClick={() => handleSort('fg_pct')}
          >
            FG% {sortBy === 'fg_pct' && (sortOrder === 'asc' ? '↑' : '↓')}
          </button>
          <button 
            className={`sort-btn ${sortBy === 'games' ? 'active' : ''}`}
            onClick={() => handleSort('games')}
          >
            Games {sortBy === 'games' && (sortOrder === 'asc' ? '↑' : '↓')}
          </button>
        </div>
      </div>

      {/* Players Display */}
      {viewMode === 'table' ? (
        <div className="table-container">
          <div className="table-wrapper">
            <table className="players-table">
              <thead>
                <tr>
                  <th onClick={() => handleSort('name')} className="sortable">
                    Player {sortBy === 'name' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('team')} className="sortable">
                    Team {sortBy === 'team' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('position')} className="sortable">
                    Position {sortBy === 'position' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th>Age</th>
                  <th onClick={() => handleSort('ppg')} className="sortable">
                    PPG {sortBy === 'ppg' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('apg')} className="sortable">
                    APG {sortBy === 'apg' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('rpg')} className="sortable">
                    RPG {sortBy === 'rpg' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('spg')} className="sortable">
                    SPG {sortBy === 'spg' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('bpg')} className="sortable">
                    BPG {sortBy === 'bpg' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('fg_pct')} className="sortable">
                    FG% {sortBy === 'fg_pct' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('fg3_pct')} className="sortable">
                    3P% {sortBy === 'fg3_pct' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('ft_pct')} className="sortable">
                    FT% {sortBy === 'ft_pct' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th onClick={() => handleSort('games')} className="sortable">
                    Games {sortBy === 'games' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th className="favorite-header">Favorite</th>
                </tr>
              </thead>
              <tbody>
                {sortedPlayers.map((player, index) => (
                  <tr key={player.id || index}>
                    <td className="player-name-cell">
                      <strong>{player.name}</strong>
                    </td>
                    <td>
                      <span className="team-badge-table">{player.team}</span>
                    </td>
                    <td>
                      <span className="position-badge-table">{player.position}</span>
                    </td>
                    <td>{player.age}</td>
                    <td className="stat-cell">{player.stats?.ppg_last?.toFixed(1) || '0.0'}</td>
                    <td className="stat-cell">{player.stats?.apg_last?.toFixed(1) || '0.0'}</td>
                    <td className="stat-cell">{player.stats?.rpg_last?.toFixed(1) || '0.0'}</td>
                    <td className="stat-cell">{player.stats?.spg_last?.toFixed(1) || '0.0'}</td>
                    <td className="stat-cell">{player.stats?.bpg_last?.toFixed(1) || '0.0'}</td>
                    <td className="stat-cell">{player.stats?.fg_pct_last?.toFixed(1) || '0.0'}%</td>
                    <td className="stat-cell">{player.stats?.fg3_pct_last?.toFixed(1) || '0.0'}%</td>
                    <td className="stat-cell">{player.stats?.ft_pct_last?.toFixed(1) || '0.0'}%</td>
                    <td className="stat-cell">{player.stats?.games_played || 0}</td>
                    <td className="favorite-cell">
                      <button
                        className={`favorite-btn ${favorites.has(player.id) ? 'favorited' : ''}`}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleFavoriteToggle(player);
                        }}
                        title={favorites.has(player.id) ? 'Remove from favorites' : 'Add to favorites'}
                      >
                        {favorites.has(player.id) ? '⭐' : '☆'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="players-grid">
          {sortedPlayers.map(player => (
            <div key={player.id} className="player-card">
              <div className="player-header">
                <div className="player-header-top">
                  <h3 className="player-name">{player.name}</h3>
                  <button
                    className={`favorite-btn-card ${favorites.has(player.id) ? 'favorited' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleFavoriteToggle(player);
                    }}
                    title={favorites.has(player.id) ? 'Remove from favorites' : 'Add to favorites'}
                  >
                    {favorites.has(player.id) ? '⭐' : '☆'}
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
                  <span>Height: {Math.floor(player.height / 12)}'{player.height % 12}"</span>
                  <span>Weight: {player.weight} lbs</span>
                </div>
              </div>

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
                  <div className="stat-item">
                    <span className="stat-label">3P%</span>
                    <span className="stat-value">{player.stats?.fg3_pct_last?.toFixed(1) || '0.0'}%</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">FT%</span>
                    <span className="stat-value">{player.stats?.ft_pct_last?.toFixed(1) || '0.0'}%</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Games</span>
                    <span className="stat-value">{player.stats?.games_played || 0}</span>
                  </div>
                </div>
              </div>

              <div className="player-trends">
                <h4>Performance Trends</h4>
                <div className="trends-grid">
                  <div className="trend-item">
                    <span className="trend-label">Consistency</span>
                    <span className="trend-value">{player.trends?.consistency_score?.toFixed(2) || '0.00'}</span>
                  </div>
                  <div className="trend-item">
                    <span className="trend-label">PPG Trend</span>
                    <span className={`trend-value ${(player.trends?.ppg_trend || 0) > 0 ? 'positive' : 'negative'}`}>
                      {(player.trends?.ppg_trend || 0) > 0 ? '+' : ''}{player.trends?.ppg_trend?.toFixed(1) || '0.0'}
                    </span>
                  </div>
                  <div className="trend-item">
                    <span className="trend-label">Games Played</span>
                    <span className="trend-value">{player.stats?.games_played || 0}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      <div className="pagination">
        <div className="pagination-controls">
          <button 
            onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
            disabled={currentPage === 1}
            className="pagination-btn"
          >
            ← Previous
          </button>
          
          <div className="pagination-info">
            <div className="page-info-main">
              <span className="page-label">Page</span>
              <span className="page-current">{currentPage}</span>
              <span className="page-separator">of</span>
              <span className="page-total">{totalPages}</span>
            </div>
            <div className="page-count-info">
              Showing {sortedPlayers.length > 0 ? (currentPage - 1) * 100 + 1 : 0} - {Math.min(currentPage * 100, (currentPage - 1) * 100 + sortedPlayers.length)} of {totalPlayers} players
            </div>
          </div>
          
          <button 
            onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
            disabled={currentPage === totalPages}
            className="pagination-btn"
          >
            Next →
          </button>
        </div>
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
