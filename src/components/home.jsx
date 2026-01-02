import React, { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import "./home.css";
import AIPredictions from "./AIPredictions";

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
        <div className="header-profile">
          <button className="profile-btn" onClick={() => alert('Profile button clicked!')}>
            <img src="/images/profile_image.jpg" alt="Profile" className="profile-img" />
          </button>
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
        </div>
      </section>

      <section id="ai-predictions" className="ai-section">
        <div className="ai-content">
          <h2>AI Predictions</h2>
          <AIPredictions />
        </div>
      </section>
    </div>
  );
};

export default Home;