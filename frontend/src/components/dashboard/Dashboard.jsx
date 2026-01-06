import { useNavigate } from 'react-router-dom';
import Layout from '../common/Layout';

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <Layout>
      <div className="space-y-8">
        {/* Hero Section */}
        <div className="bg-gradient-to-br from-white via-white to-primary-50/30 rounded-2xl shadow-2xl shadow-primary-900/10 p-10 border border-primary-100/50">
          <h2 className="text-4xl font-display font-bold bg-gradient-to-r from-primary-700 to-primary-500 bg-clip-text text-transparent mb-4 tracking-tight">
            Welcome to Oregon Grant Automation
          </h2>
          <p className="text-gray-600 text-lg leading-relaxed">
            Your intelligent grant discovery and application assistant for Oregon preschools and child care providers.
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="group bg-gradient-to-br from-primary-50 to-primary-100/50 border-2 border-primary-200/60 rounded-2xl p-7 shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 hover:border-primary-300">
            <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform">
              <span className="text-2xl">🔍</span>
            </div>
            <h3 className="text-xl font-display font-bold text-primary-700 mb-3">
              Grant Discovery
            </h3>
            <p className="text-gray-700 leading-relaxed">
              Find grants from Oregon sources to support your programs
            </p>
          </div>

          <div className="group bg-gradient-to-br from-accent-50 to-accent-100/50 border-2 border-accent-400/60 rounded-2xl p-7 shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 hover:border-accent-500">
            <div className="w-12 h-12 bg-gradient-to-br from-accent-400 to-accent-600 rounded-xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform">
              <span className="text-2xl">✨</span>
            </div>
            <h3 className="text-xl font-display font-bold text-primary-700 mb-3">
              Smart Matching
            </h3>
            <p className="text-gray-700 leading-relaxed">
              Grants matched to your organization's needs and eligibility
            </p>
          </div>

          <div className="group bg-gradient-to-br from-primary-50 to-primary-100/50 border-2 border-primary-200/60 rounded-2xl p-7 shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 hover:border-primary-300">
            <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform">
              <span className="text-2xl">⚡</span>
            </div>
            <h3 className="text-xl font-display font-bold text-primary-700 mb-3">
              Application Generation
            </h3>
            <p className="text-gray-700 leading-relaxed">
              Generate professional grant applications instantly
            </p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <h3 className="text-2xl font-display font-bold text-gray-900 mb-6">
            Quick Actions
          </h3>
          <div className="space-y-4">
            <button
              onClick={() => navigate('/grants')}
              className="group w-full bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white px-8 py-5 rounded-xl text-left font-semibold shadow-lg shadow-primary-500/30 transition-all duration-300 hover:shadow-2xl hover:shadow-primary-500/40 hover:scale-[1.02] flex items-center justify-between"
            >
              <span className="text-lg">Browse Available Grants</span>
              <span className="text-2xl group-hover:translate-x-2 transition-transform">→</span>
            </button>
            <button className="w-full bg-gradient-to-r from-gray-100 to-gray-200 text-gray-400 px-8 py-5 rounded-xl text-left font-semibold cursor-not-allowed opacity-60">
              <span className="text-lg">Set Up Your Organization Profile</span>
              <span className="text-sm ml-2">(Coming Soon)</span>
            </button>
            <button className="w-full bg-gradient-to-r from-gray-100 to-gray-200 text-gray-400 px-8 py-5 rounded-xl text-left font-semibold cursor-not-allowed opacity-60">
              <span className="text-lg">View My Applications</span>
              <span className="text-sm ml-2">(Coming Soon)</span>
            </button>
          </div>
        </div>

        {/* Call to Action */}
        <div className="bg-gradient-to-r from-accent-400 to-accent-500 rounded-2xl shadow-2xl shadow-accent-500/30 p-8 border-2 border-accent-600">
          <div className="flex items-start gap-4">
            <div className="text-4xl">🎯</div>
            <div>
              <h4 className="text-2xl font-display font-bold text-white mb-3">
                Ready to Get Started!
              </h4>
              <p className="text-gray-900 text-lg leading-relaxed">
                Browse 8 realistic Oregon grants including Preschool Promise Program, Child Care Infrastructure Fund, and more. Click "Browse Available Grants" to explore and start applying!
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
