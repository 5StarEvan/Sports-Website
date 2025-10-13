import React from "react";
import "./home.css";
import AIPredictions from "./AIPredictions";

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
          <a href="#ai-predictions">AI PREDICTIONS</a>
          <a href="#stats">STATS</a>
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
        <AIPredictions />
      </section>
    </div>
  );
};

export default Home;