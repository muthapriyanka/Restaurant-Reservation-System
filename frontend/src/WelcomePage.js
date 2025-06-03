import React from 'react';
import { useNavigate } from 'react-router-dom';

const WelcomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="welcome-bg">
      <div className="welcome-overlay">
        <div className="welcome-content">
          <h1 className="welcome-heading">🍽️ Welcome to BookTable</h1>
          <p className="welcome-description">
            BookTable is your all-in-one solution for managing restaurant reservations. Whether you're a restaurant owner or a diner, we’ve got you covered.
          </p>
          <div className="welcome-buttons">
            <button className="btn login-btn" onClick={() => navigate('/login')}>Login</button>
            <button className="btn register-btn" onClick={() => navigate('/register')}>Register</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomePage;
