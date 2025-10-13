import React, { useEffect, useState } from "react";

const AIPredictions = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const API_URL = "http://127.0.0.1:5000/api/predictions";

    const fetchPredictions = async () => {
      try {
        const response = await fetch(API_URL);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setPredictions(data.data); // <-- get the array inside `data`
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

  return (
    <div className="ai-predictions-container">
      {predictions.length === 0 ? (
        <p>No predictions available.</p>
      ) : (
        <ul>
          {predictions.map((prediction, index) => (
            <li key={index}>
              <strong>{prediction.team}</strong>: {prediction.prediction}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AIPredictions;
