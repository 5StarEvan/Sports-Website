import React, { useEffect, useState } from "react";

const AIPredictions = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const API_URL = "http://127.0.0.1:5000/api/ai-predictions";
    const fetchPredictions = async () => {
      try {
        const response = await fetch(API_URL);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // data = { predictions: { top_scorers: [...], top_assists: [...], ... } }
        setPredictions(data?.predictions?.top_scorers ?? []);
      } catch (err) {
        console.error("Failed to fetch predictions:", err);
        setError("Failed to connect to AI server. Make sure the backend is running.");
      } finally {
        setLoading(false);
      }
    };

    fetchPredictions();
  }, []);

  if (loading) return <div>Loading AI predictions...</div>;
  if (error) return <div>{error}</div>;
  if (!Array.isArray(predictions)) return <div>No predictions available.</div>;

  return (
    <div className="ai-predictions-container">
      {predictions.length === 0 ? (
        <p>No predictions available.</p>
      ) : (
        <ul>
          {predictions.map((player, index) => (
            <li key={index}>
              <strong>{player.PLAYER_NAME}</strong>: {player.PREDICTED_PPG?.toFixed ? player.PREDICTED_PPG.toFixed(1) : player.PREDICTED_PPG} PPG
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AIPredictions;
