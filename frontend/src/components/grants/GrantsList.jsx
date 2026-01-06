import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { Calendar, DollarSign, MapPin, Award } from 'lucide-react';
import Layout from '../common/Layout';

export default function GrantsList() {
  const [grants, setGrants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchGrants();
  }, []);

  const fetchGrants = async () => {
    try {
      setLoading(true);
      const response = await api.get('/grants');
      setGrants(response.data.grants);
    } catch (err) {
      setError('Failed to load grants. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const getDaysUntilDeadline = (deadline) => {
    const now = new Date();
    const deadlineDate = new Date(deadline);
    const diff = Math.ceil((deadlineDate - now) / (1000 * 60 * 60 * 24));
    return diff;
  };

  const getDeadlineColor = (days) => {
    if (days <= 7) return 'text-red-600 bg-red-50';
    if (days <= 30) return 'text-orange-600 bg-orange-50';
    return 'text-green-600 bg-green-50';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading grants...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600">{error}</p>
          <button
            onClick={fetchGrants}
            className="mt-4 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <Layout>
      <div className="space-y-8">
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-2xl shadow-xl shadow-primary-500/30 p-6 border border-primary-500">
        <h3 className="text-lg font-display font-bold text-white mb-2">
          🎯 {grants.length} Oregon Grants Available
        </h3>
        <p className="text-primary-100">
          These are sample grants for testing. In Phase 2, we'll automatically discover real grants weekly.
        </p>
      </div>

      <div className="grid gap-6">
        {grants.map((grant) => {
          const daysLeft = getDaysUntilDeadline(grant.deadline);
          return (
            <div
              key={grant.id}
              className="bg-white rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 p-8 border border-gray-100 hover:scale-[1.02] hover:border-primary-200"
            >
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <h3 className="text-xl font-display font-bold text-gray-900 mb-2 tracking-tight">
                    {grant.title}
                  </h3>
                  <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
                    <Award className="w-4 h-4" />
                    <span>{grant.source_name}</span>
                    <span className="text-gray-400">•</span>
                    <span className="capitalize">{grant.source_type}</span>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDeadlineColor(daysLeft)}`}>
                  {daysLeft > 0 ? `${daysLeft} days left` : 'Deadline passed'}
                </span>
              </div>

              <p className="text-gray-700 mb-4 line-clamp-3">{grant.description}</p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div className="flex items-center gap-2 text-sm">
                  <DollarSign className="w-4 h-4 text-green-600" />
                  <span className="font-medium">
                    {formatCurrency(grant.amount_min)} - {formatCurrency(grant.amount_max)}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Calendar className="w-4 h-4 text-blue-600" />
                  <span>Deadline: {formatDate(grant.deadline)}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <MapPin className="w-4 h-4 text-purple-600" />
                  <span className="capitalize">{grant.geographic_restriction || 'Statewide'}</span>
                </div>
              </div>

              {grant.funding_priorities && grant.funding_priorities.length > 0 && (
                <div className="mb-4">
                  <p className="text-sm font-medium text-gray-700 mb-2">Funding Priorities:</p>
                  <div className="flex flex-wrap gap-2">
                    {grant.funding_priorities.slice(0, 3).map((priority, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 bg-gray-100 text-gray-700 rounded-md text-xs"
                      >
                        {priority}
                      </span>
                    ))}
                    {grant.funding_priorities.length > 3 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded-md text-xs">
                        +{grant.funding_priorities.length - 3} more
                      </span>
                    )}
                  </div>
                </div>
              )}

              <div className="flex gap-4">
                <button
                  onClick={() => navigate(`/grants/${grant.id}`)}
                  className="flex-1 px-6 py-3 bg-white text-primary-700 border-2 border-primary-500 rounded-xl hover:bg-primary-50 font-semibold transition-all duration-200 hover:scale-105 hover:shadow-lg"
                >
                  View Details
                </button>
                <button
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-xl hover:from-primary-700 hover:to-primary-800 font-semibold shadow-lg shadow-primary-500/30 transition-all duration-200 hover:shadow-xl hover:shadow-primary-500/40 hover:scale-105"
                  onClick={() => navigate(`/applications/new/${grant.id}`)}
                >
                  Apply Now
                </button>
              </div>
            </div>
          );
        })}
      </div>
      </div>
    </Layout>
  );
}
