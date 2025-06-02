import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useUser } from '../../context/UserContext';

const Header: React.FC = () => {
  const { user, logout } = useUser();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <Link to="/home">
                <img
                  className="h-10 w-auto"
                  src="/assets/FitGenieLogo.png"
                  alt="FitGenie"
                />
              </Link>
            </div>
            <nav className="ml-6 flex space-x-8">
              <Link
                to="/home"
                className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-secondary-grey hover:text-secondary-navy hover:border-primary-blue"
              >
                Dashboard
              </Link>
              <Link
                to="/meal-plan"
                className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-secondary-grey hover:text-secondary-navy hover:border-primary-blue"
              >
                Meal Plan
              </Link>
              <Link
                to="/workout-plan"
                className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-secondary-grey hover:text-secondary-navy hover:border-primary-blue"
              >
                Workout Plan
              </Link>
              <Link
                to="/chatbot"
                className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-secondary-grey hover:text-secondary-navy hover:border-primary-blue"
              >
                AI Assistant
              </Link>
            </nav>
          </div>
          <div className="flex items-center">
            <Link
              to="/profile"
              className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-secondary-navy bg-secondary-mint bg-opacity-20 hover:bg-opacity-30"
            >
              Profile
            </Link>
            <button
              onClick={handleLogout}
              className="ml-4 inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-secondary-grey hover:text-secondary-navy"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
