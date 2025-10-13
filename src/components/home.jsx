import React from "react";
import { Link } from "react-router-dom";
import "./home.css";
import AIPredictions from "./AIPredictions";
import DebugPanel from "./DebugPanel";
import ErrorBoundary from "./ErrorBoundary";

const Home = () => {
  return (
    <div className="main-wrapper">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <span className="basketball-icon">🏀</span>
          <span className="header-title">BASKETBALL AGENDA</span>
        </div>
        <nav className="header-nav">
          <Link to="/stats">STATS</Link>
          <a href="#recommendations">RECOMMENDATIONS</a>
          <a href="#favourites">FAVOURITES</a>
        </nav>
        <div className="header-profile">
          <button className="profile-btn" onClick={() => alert('Profile button clicked!')}>
            <img src="/images/profile_image.jpg" alt="Profile" className="profile-img" />
          </button>
        </div>
      </header>

      <section className="hero-split-bg">
        <div className="hero-center-content">
          <div className="hero-image-center">
            <img src="/images/home_jordan_logo.png" alt="Center" style={{ maxWidth: "100%", maxHeight: "100%" }} />
          </div>
          <h1 className="hero-title">
            <span className="black-word">BASKET</span><span className="highlight">BALL</span> AGENDA
          </h1>
        </div>
      </section>

      {/* AI Predictions Section */}
      <section id="ai-predictions" className="ai-section">
        {/* Temporarily disabled to avoid blank screen while backend is unreachable */}
        {/* <ErrorBoundary>
          <AIPredictions />
        </ErrorBoundary> */}
        <div style={{ color: '#fff' }}>AI Predictions temporarily disabled. Check Debug Panel.</div>
      </section>

      <DebugPanel />
    </div>
  );
};

export default Home;