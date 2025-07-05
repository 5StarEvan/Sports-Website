import React, { useState, useEffect } from 'react';
import { Trophy, TrendingUp, Users, Calendar, Star, Activity, Target, Award, Play, BarChart3, Globe, Zap } from 'lucide-react';
import '../components/home.css'; 

const HomePage = () => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [activeFeature, setActiveFeature] = useState(0);
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    setIsLoaded(true);
    
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const features = [
    {
      icon: <BarChart3 className="w-8 h-8" />,
      title: "Live Statistics",
      description: "Real-time sports data and analytics"
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Team Analytics",
      description: "Comprehensive team performance metrics"
    },
    {
      icon: <Trophy className="w-8 h-8" />,
      title: "Tournament Tracking",
      description: "Follow your favorite tournaments"
    },
    {
      icon: <Activity className="w-8 h-8" />,
      title: "Player Insights",
      description: "Deep dive into player statistics"
    }
  ];

  const stats = [
    { label: "Active Sports", value: "15+", icon: <Globe className="w-6 h-6" /> },
    { label: "Teams Tracked", value: "2,500+", icon: <Users className="w-6 h-6" /> },
    { label: "Live Matches", value: "24/7", icon: <Play className="w-6 h-6" /> },
    { label: "Data Points", value: "1M+", icon: <BarChart3 className="w-6 h-6" /> }
  ];

  const sports = [
    { name: "Basketball", icon: "🏀", color: "from-orange-500 to-red-500" },
    { name: "Football", icon: "🏈", color: "from-blue-500 to-purple-500" },
    { name: "Soccer", icon: "⚽", color: "from-green-500 to-blue-500" },
    { name: "Tennis", icon: "🎾", color: "from-yellow-500 to-green-500" },
    { name: "Baseball", icon: "⚾", color: "from-red-500 to-pink-500" },
    { name: "Hockey", icon: "🏒", color: "from-cyan-500 to-blue-500" }
  ];

  return (
    <div className="homepage">
      <nav className={`navbar ${isLoaded ? 'loaded' : ''}`}>
        <div className="nav-container">
          <div className="nav-logo">
            <div className="logo-icon">
              <Zap className="w-8 h-8" />
            </div>
            <span className="logo-text">SportsPro</span>
          </div>
          <ul className="nav-menu">
            <li><a href="#home" className="nav-link">Home</a></li>
            <li><a href="#sports" className="nav-link">Sports</a></li>
            <li><a href="#stats" className="nav-link">Statistics</a></li>
            <li><a href="#teams" className="nav-link">Teams</a></li>
            <li><a href="#players" className="nav-link">Players</a></li>
            <li><a href="#live" className="nav-link live-btn">
              <div className="live-indicator"></div>
              Live
            </a></li>
          </ul>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-background">
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
          <div className="gradient-orb orb-3"></div>
          <div className="floating-elements">
            {sports.map((sport, index) => (
              <div 
                key={index}
                className={`floating-ball ball-${index + 1}`}
                style={{ '--delay': `${index * 0.5}s` }}
              >
                {sport.icon}
              </div>
            ))}
          </div>
        </div>
        
        <div className="hero-content">
          <div className={`hero-badge ${isLoaded ? 'animate-in' : ''}`}>
            <Star className="w-4 h-4" />
            <span>Professional Sports Analytics</span>
          </div>
          
          <h1 className={`hero-title ${isLoaded ? 'animate-in' : ''}`}>
            The Future of
            <span className="gradient-text"> Sports Statistics</span>
          </h1>
          
          <p className={`hero-subtitle ${isLoaded ? 'animate-in' : ''}`}>
            Experience real-time sports analytics like never before. Track your favorite teams, 
            players, and tournaments with our cutting-edge platform.
          </p>
          
          <div className={`hero-actions ${isLoaded ? 'animate-in' : ''}`}>
            <button className="cta-button primary">
              <Play className="w-5 h-5" />
              Start Exploring
            </button>
            <button className="cta-button secondary">
              <BarChart3 className="w-5 h-5" />
              View Demo
            </button>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="scroll-indicator">
          <div className="scroll-arrow"></div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-container">
          {stats.map((stat, index) => (
            <div 
              key={index}
              className={`stat-card ${isLoaded ? 'animate-in' : ''}`}
              style={{ '--delay': `${index * 0.1}s` }}
            >
              <div className="stat-icon">
                {stat.icon}
              </div>
              <div className="stat-content">
                <div className="stat-value">{stat.value}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="features-container">
          <div className="features-header">
            <h2 className="section-title">
              Powerful Features for
              <span className="gradient-text"> Every Sport</span>
            </h2>
            <p className="section-subtitle">
              Our platform provides comprehensive analytics and insights for all major sports
            </p>
          </div>
          
          <div className="features-grid">
            {features.map((feature, index) => (
              <div 
                key={index}
                className={`feature-card ${activeFeature === index ? 'active' : ''}`}
                onMouseEnter={() => setActiveFeature(index)}
              >
                <div className="feature-icon">
                  {feature.icon}
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
                <div className="feature-arrow">
                  <TrendingUp className="w-5 h-5" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Sports Grid */}
      <section className="sports-section">
        <div className="sports-container">
          <h2 className="section-title">
            Sports We Cover
          </h2>
          <div className="sports-grid">
            {sports.map((sport, index) => (
              <div 
                key={index}
                className="sport-card"
                style={{ '--delay': `${index * 0.1}s` }}
              >
                <div className={`sport-gradient bg-gradient-to-br ${sport.color}`}></div>
                <div className="sport-icon">{sport.icon}</div>
                <h3 className="sport-name">{sport.name}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-container">
          <div className="cta-content">
            <h2 className="cta-title">
              Ready to Elevate Your Sports Experience?
            </h2>
            <p className="cta-subtitle">
              Join thousands of sports enthusiasts who trust SportsPro for their analytics needs
            </p>
            <button className="cta-button primary large">
              <Award className="w-6 h-6" />
              Get Started Now
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;