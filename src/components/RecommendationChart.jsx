import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import './Recommendations.css';

const RecommendationChart = () => {
    const { stat } = useParams();
    const [players, setPlayers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const API_BASE_URL = '/api';

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                setLoading(true);
                const response = await fetch(`${API_BASE_URL}/recommendations/${stat}`);

                if (!response.ok) {
                    throw new Error(`Failed to fetch recommendations: ${response.status}`);
                }

                const data = await response.json();
                const list = Array.isArray(data) ? data : (data?.[stat] ?? []);
                setPlayers(list);
                setError(null);
            } catch (err) {
                console.error('Error fetching recommendations:', err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, [stat]);

    if (loading) {
        return <div className="loading">Loading recommendations...</div>;
    }

    if (error) {
        return <div className="error">Error: {error}</div>;
    }

    const predictedKey = `PREDICTED_${stat}`;
    const lastKey = `${stat}_LAST`;
    const improvementKey = `${stat}_IMPROVEMENT`;

    return (
        <div className="recommendations-wrapper">
            <header className="recommendations-header">
                <Link to="/recommendations" className="back-link">← Back to Recommendations</Link>
                <h1 className="recommendations-title">
                    Top {stat} Improvement %
                </h1>
            </header>

            <div className="recommendations-content">
                {players.length === 0 ? (
                    <p className="section-description">No recommendations available yet.</p>
                ) : (
                    <div className="recommendations-grid">
                        {players.map((player, index) => {
                            const improvement = Number(player[improvementKey] ?? 0);
                            return (
                            <div key={player.PLAYER_NAME ?? index} className="recommendation-card">
                                <div className="card-header">
                                    <span className="rank-badge">#{index + 1}</span>
                                    <span className="category-badge">{player.TEAM}</span>
                                </div>
                                <div className="card-body">
                                    <h3 className="insight-title">{player.PLAYER_NAME}</h3>
                                    <p className="recommendation-reason">
                                        {improvement >= 0 ? '+' : ''}{improvement.toFixed(1)}% {stat} improvement
                                    </p>
                                    <p className="details-text">
                                        {Number(player[lastKey] ?? 0).toFixed(1)} → {Number(player[predictedKey] ?? 0).toFixed(1)} {stat}
                                    </p>
                                </div>
                            </div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
};

export default RecommendationChart;
