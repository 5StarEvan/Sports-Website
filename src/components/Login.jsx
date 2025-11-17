import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Login.css";

const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle login logic here
    console.log("Login attempt:", formData);
  };

  return (
    <div className="login-wrapper">
      <div className="login-container">
        <div className="login-header">
          <span className="basketball-icon">🏀</span>
          <h1 className="login-title">LOGIN</h1>
        </div>
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">EMAIL</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="Enter your email"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">PASSWORD</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter your password"
            />
          </div>
          <button type="submit" className="login-submit-btn">
            LOGIN
          </button>
        </form>
        <div className="login-footer">
          <p>
            Don't have an account?{" "}
            <Link to="/create-account" className="login-link">
              Create Account
            </Link>
          </p>
          <Link to="/" className="login-link">
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;

