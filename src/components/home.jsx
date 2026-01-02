import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./home.css";
import AIPredictions from "./AIPredictions";
import { isAuthenticated, getUser, logout } from "../utils/auth";

const BasketballAnimation = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    class Basketball {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 30 + 20;
        this.speedX = (Math.random() - 0.5) * 2;
        this.speedY = (Math.random() - 0.5) * 2;
        this.rotation = Math.random() * Math.PI * 2;
        this.rotationSpeed = (Math.random() - 0.5) * 0.05;
        this.opacity = Math.random() * 0.3 + 0.1;
      }

      update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.rotation += this.rotationSpeed;

        if (this.x < -this.size) this.x = canvas.width + this.size;
        if (this.x > canvas.width + this.size) this.x = -this.size;
        if (this.y < -this.size) this.y = canvas.height + this.size;
        if (this.y > canvas.height + this.size) this.y = -this.size;
      }

      draw() {
        ctx.save();
        ctx.globalAlpha = this.opacity;
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);

        ctx.beginPath();
        ctx.arc(0, 0, this.size, 0, Math.PI * 2);
        ctx.fillStyle = '#ff6b35';
        ctx.fill();

        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        
        ctx.beginPath();
        ctx.moveTo(-this.size, 0);
        ctx.lineTo(this.size, 0);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, -this.size);
        ctx.lineTo(0, this.size);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(0, 0, this.size, -Math.PI / 4, Math.PI / 4);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(0, 0, this.size, Math.PI * 3 / 4, Math.PI * 5 / 4);
        ctx.stroke();

        ctx.restore();
      }
    }

    const basketballs = [];
    for (let i = 0; i < 15; i++) {
      basketballs.push(new Basketball());
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      basketballs.forEach(ball => {
        ball.update();
        ball.draw();
      });

      requestAnimationFrame(animate);
    }

    animate();

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="basketball-canvas"
    />
  );
};

const Home = () => {
  const navigate = useNavigate();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const checkAuth = () => {
      const authenticated = isAuthenticated();
      setIsLoggedIn(authenticated);
      if (authenticated) {
        setUser(getUser());
      }
    };

    checkAuth();
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };

    if (isDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isDropdownOpen]);

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleLogout = async () => {
    await logout();
    setIsLoggedIn(false);
    setUser(null);
    setIsDropdownOpen(false);
    navigate("/");
  };

  return (
    <div className="main-wrapper">
      <BasketballAnimation />

      <header className="header">
        <div className="header-left">
          <span className="basketball-icon">🏀</span>
          <span className="header-title">BASKETBALL AGENDA</span>
        </div>
        <nav className="header-nav">
          <Link to="/stats">STATS</Link>
          <Link to="/recommendations">RECOMMENDATIONS</Link>
          <Link to="/favourites">FAVOURITES</Link>
        </nav>
        <div className="header-profile" ref={dropdownRef}>
          <button className="profile-btn" onClick={toggleDropdown}>
            {isLoggedIn && user ? (
              <div className="profile-initials">
                {user.first_name?.[0]?.toUpperCase() || ''}{user.last_name?.[0]?.toUpperCase() || ''}
              </div>
            ) : (
              <img src="/images/profile_image.jpg" alt="Profile" className="profile-img" />
            )}
          </button>
          {isDropdownOpen && (
            <div className="profile-dropdown">
              {isLoggedIn && user ? (
                <>
                  <div className="dropdown-user-info">
                    <div className="dropdown-user-name">
                      {user.first_name} {user.last_name}
                    </div>
                    <div className="dropdown-user-email">{user.email}</div>
                  </div>
                  <div className="dropdown-divider"></div>
                  <Link to="/favourites" className="dropdown-item" onClick={() => setIsDropdownOpen(false)}>
                    My Favourites
                  </Link>
                  <Link to="/recommendations" className="dropdown-item" onClick={() => setIsDropdownOpen(false)}>
                    Recommendations
                  </Link>
                  <div className="dropdown-divider"></div>
                  <button className="dropdown-item logout-btn" onClick={handleLogout}>
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="dropdown-item" onClick={() => setIsDropdownOpen(false)}>
                    Login
                  </Link>
                  <Link to="/create-account" className="dropdown-item" onClick={() => setIsDropdownOpen(false)}>
                    Create Account
                  </Link>
                </>
              )}
            </div>
          )}
        </div>
      </header>

      <section className="hero-split-bg">
        <div className="hero-center-content">
          <div className="hero-image-center">
            <BasketballAnimation />
          </div>
          <h1 className="hero-title">
            <span className="black-word">BASKET</span>
            <span className="highlight">BALL</span> AGENDA
          </h1>
          <p className="hero-subtitle">
            Your Ultimate Destination for Basketball Insights, Stats, and AI-Powered Predictions
          </p>
          <div className="hero-cta">
            <Link to="/stats" className="cta-button primary">
              Explore Stats
            </Link>
            <Link to="/recommendations" className="cta-button secondary">
              Get Recommendations
            </Link>
          </div>
        </div>
      </section>

      <section className="featured-section">
        <div className="featured-container">
          <h2 className="section-title">Trending Now</h2>
          <p className="section-description">
            Stay ahead with the latest games, player performances, and breaking news
          </p>
          <div className="featured-grid">
            <div className="featured-card">
              <div className="featured-badge">LIVE</div>
              <div className="featured-content">
                <h3>Lakers vs Warriors</h3>
                <p className="featured-score">112 - 108</p>
                <p className="featured-time">Q4 - 2:34 remaining</p>
                <Link to="/stats" className="featured-link">View Details →</Link>
              </div>
            </div>
            <div className="featured-card">
              <div className="featured-badge upcoming">UPCOMING</div>
              <div className="featured-content">
                <h3>Celtics vs Heat</h3>
                <p className="featured-date">Tonight at 8:00 PM EST</p>
                <p className="featured-prediction">AI Prediction: Celtics 65%</p>
                <Link to="/recommendations" className="featured-link">Get Prediction →</Link>
              </div>
            </div>
            <div className="featured-card">
              <div className="featured-badge highlight">HIGHLIGHT</div>
              <div className="featured-content">
                <h3>Player of the Week</h3>
                <p className="featured-player">LeBron James</p>
                <p className="featured-stats">32.5 PPG | 8.2 RPG | 7.1 APG</p>
                <Link to="/stats" className="featured-link">View Stats →</Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="how-it-works-section">
        <div className="how-it-works-container">
          <h2 className="section-title">How It Works</h2>
          <p className="section-description">
            Get started in three simple steps and unlock the power of AI-driven basketball insights
          </p>
          <div className="steps-container">
            <div className="step-item">
              <div className="step-number">01</div>
              <div className="step-content">
                <h3>Create Your Account</h3>
                <p>Sign up in seconds and personalize your experience with your favorite teams and players.</p>
              </div>
            </div>
            <div className="step-connector"></div>
            <div className="step-item">
              <div className="step-number">02</div>
              <div className="step-content">
                <h3>Explore & Analyze</h3>
                <p>Dive into comprehensive statistics, AI predictions, and personalized recommendations.</p>
              </div>
            </div>
            <div className="step-connector"></div>
            <div className="step-item">
              <div className="step-number">03</div>
              <div className="step-content">
                <h3>Stay Ahead</h3>
                <p>Get real-time updates, save favorites, and make informed decisions with cutting-edge insights.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="ai-predictions" className="ai-section">
        <div className="ai-content">
          <h2 className="section-title">AI Predictions</h2>
          <p className="section-description">
            Get ahead of the game with our cutting-edge AI predictions powered by advanced analytics
          </p>
          <AIPredictions />
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-container">
          <h2 className="cta-title">Ready to Elevate Your Basketball Experience?</h2>
          <p className="cta-description">
            Join thousands of basketball enthusiasts and get access to exclusive insights, predictions, and more.
          </p>
          <div className="cta-buttons">
            <Link to="/login" className="cta-button primary large">
              Get Started
            </Link>
            <Link to="/create-account" className="cta-button secondary large">
              Create Account
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;