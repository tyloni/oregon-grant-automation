import { useAuth } from '../../hooks/useAuth.jsx';
import { useNavigate, useLocation } from 'react-router-dom';

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-primary-50/30 to-gray-100">
      <nav className="bg-white/80 backdrop-blur-lg shadow-lg border-b-3 border-accent-500 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20">
            <div className="flex items-center">
              <h1
                className="text-2xl font-display font-bold bg-gradient-to-r from-primary-700 to-primary-500 bg-clip-text text-transparent cursor-pointer hover:from-primary-600 hover:to-primary-400 transition-all tracking-tight"
                onClick={() => navigate('/dashboard')}
              >
                Oregon Grant Automation
              </h1>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={() => navigate('/dashboard')}
                className={`px-5 py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 ${
                  isActive('/dashboard')
                    ? 'bg-gradient-to-r from-primary-600 to-primary-700 text-white shadow-lg shadow-primary-500/30 scale-105'
                    : 'text-gray-700 hover:bg-primary-50 hover:text-primary-700 hover:scale-105'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => navigate('/grants')}
                className={`px-5 py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 ${
                  isActive('/grants')
                    ? 'bg-gradient-to-r from-primary-600 to-primary-700 text-white shadow-lg shadow-primary-500/30 scale-105'
                    : 'text-gray-700 hover:bg-primary-50 hover:text-primary-700 hover:scale-105'
                }`}
              >
                Grants
              </button>
              <button
                onClick={handleLogout}
                className="px-5 py-2.5 rounded-lg text-sm font-semibold text-gray-700 hover:bg-red-50 hover:text-red-700 transition-all duration-200 hover:scale-105"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {children}
      </main>
    </div>
  );
}
