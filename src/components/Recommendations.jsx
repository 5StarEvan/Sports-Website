import React from 'react';
import { Link } from 'react-router-dom';
import './Stats.css'; // Reusing styles

const Recommendations = () => {
  return (
    <div className="stats-container">
      <div className="stats-header">
        <Link to="/" className="back-to-home">← Back to Home</Link>
        <h1>📊 Recommendations</h1>
        <p>Your personalized player recommendations will appear here</p>
      </div>
      <div style={{ textAlign: 'center', padding: '40px', color: 'rgba(255, 255, 255, 0.8)' }}>
        <p>Recommendations feature coming soon...</p>
      </div>
    </div>
  );
};

export default Recommendations;

