import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { applicationAPI } from '../../services/api';
import { ArrowLeft, Sparkles, Wand2 } from 'lucide-react';
import Layout from '../common/Layout';

export default function ApplicationForm() {
  const { grantId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [generatingField, setGeneratingField] = useState(null);

  const [formData, setFormData] = useState({
    organization_name: '',
    organization_type: 'Child Care Center',
    city: '',
    mission_statement: '',
    current_enrollment: '',
    operating_budget: '',
    staff_count: '',
    // Personalization fields
    key_achievements: '',
    specific_needs: '',
    target_outcomes: '',
    community_impact: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAutoGenerate = async (fieldName) => {
    // Validate that basic org info is filled
    if (!formData.organization_name || !formData.city || !formData.mission_statement) {
      setError('Please fill in Organization Name, City, and Mission Statement before auto-generating.');
      return;
    }

    setGeneratingField(fieldName);
    setError(null);

    try {
      const response = await applicationAPI.getPersonalizationSuggestion(fieldName, {
        organization_name: formData.organization_name,
        organization_type: formData.organization_type,
        city: formData.city,
        mission_statement: formData.mission_statement,
        current_enrollment: parseInt(formData.current_enrollment) || 0,
        operating_budget: parseFloat(formData.operating_budget) || 0,
        staff_count: parseInt(formData.staff_count) || 0
      });

      setFormData(prev => ({
        ...prev,
        [fieldName]: response.data.suggestion
      }));
    } catch (err) {
      setError(err.response?.data?.detail || `Failed to generate ${fieldName}. Please try again.`);
      console.error(err);
    } finally {
      setGeneratingField(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Convert numeric fields
      const orgData = {
        ...formData,
        current_enrollment: parseInt(formData.current_enrollment),
        operating_budget: parseFloat(formData.operating_budget),
        staff_count: parseInt(formData.staff_count)
      };

      // Generate the application
      const response = await applicationAPI.generate(parseInt(grantId), orgData);

      // Navigate to the application viewer
      navigate(`/applications/${response.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate application. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto">
        <button
          onClick={() => navigate('/grants')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Grants
        </button>

        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="flex items-center gap-3 mb-6">
            <Sparkles className="w-8 h-8 text-primary-600" />
            <div>
              <h1 className="text-2xl font-display font-bold text-gray-900 tracking-tight">Generate Grant Application</h1>
              <p className="text-gray-600 mt-1">Fill in your organization details and we'll create a tailored application</p>
            </div>
          </div>

          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="organization_name" className="block text-sm font-medium text-gray-700 mb-2">
                Organization Name *
              </label>
              <input
                type="text"
                id="organization_name"
                name="organization_name"
                required
                value={formData.organization_name}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                placeholder="e.g., Sunshine Preschool"
              />
            </div>

            <div>
              <label htmlFor="organization_type" className="block text-sm font-medium text-gray-700 mb-2">
                Organization Type *
              </label>
              <select
                id="organization_type"
                name="organization_type"
                required
                value={formData.organization_type}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="Child Care Center">Child Care Center</option>
                <option value="Preschool">Preschool</option>
                <option value="Family Child Care">Family Child Care</option>
                <option value="Head Start">Head Start</option>
                <option value="Nonprofit Organization">Nonprofit Organization</option>
              </select>
            </div>

            <div>
              <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-2">
                City *
              </label>
              <input
                type="text"
                id="city"
                name="city"
                required
                value={formData.city}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                placeholder="e.g., Portland"
              />
            </div>

            <div>
              <label htmlFor="mission_statement" className="block text-sm font-medium text-gray-700 mb-2">
                Mission Statement *
              </label>
              <textarea
                id="mission_statement"
                name="mission_statement"
                required
                value={formData.mission_statement}
                onChange={handleChange}
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                placeholder="Describe your organization's mission and values..."
              />
              <p className="text-xs text-gray-500 mt-1">This will be used to align your application with the grant's priorities</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label htmlFor="current_enrollment" className="block text-sm font-medium text-gray-700 mb-2">
                  Current Enrollment *
                </label>
                <input
                  type="number"
                  id="current_enrollment"
                  name="current_enrollment"
                  required
                  min="0"
                  value={formData.current_enrollment}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="e.g., 45"
                />
              </div>

              <div>
                <label htmlFor="operating_budget" className="block text-sm font-medium text-gray-700 mb-2">
                  Annual Budget ($) *
                </label>
                <input
                  type="number"
                  id="operating_budget"
                  name="operating_budget"
                  required
                  min="0"
                  step="0.01"
                  value={formData.operating_budget}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="e.g., 250000"
                />
              </div>

              <div>
                <label htmlFor="staff_count" className="block text-sm font-medium text-gray-700 mb-2">
                  Staff Count *
                </label>
                <input
                  type="number"
                  id="staff_count"
                  name="staff_count"
                  required
                  min="0"
                  value={formData.staff_count}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="e.g., 8"
                />
              </div>
            </div>

            {/* Personalization Section */}
            <div className="border-t-2 border-gray-200 pt-6 mt-8">
              <div className="bg-gradient-to-r from-accent-400 to-accent-500 rounded-xl p-6 mb-6">
                <h3 className="text-lg font-display font-bold text-white mb-2">✨ AI Personalization Questions</h3>
                <p className="text-gray-900 text-sm">
                  Help our AI create a more compelling application by answering these questions. The more specific you are, the better your application will be!
                </p>
              </div>

              <div className="space-y-6">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label htmlFor="key_achievements" className="block text-sm font-medium text-gray-700">
                      What are your organization's key achievements or success stories? *
                    </label>
                    <button
                      type="button"
                      onClick={() => handleAutoGenerate('key_achievements')}
                      disabled={generatingField === 'key_achievements'}
                      className="flex items-center gap-1 px-3 py-1 text-xs bg-primary-50 text-primary-700 border border-primary-300 rounded-md hover:bg-primary-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {generatingField === 'key_achievements' ? (
                        <>
                          <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-primary-700"></div>
                          Generating...
                        </>
                      ) : (
                        <>
                          <Wand2 className="w-3 h-3" />
                          Auto-Generate
                        </>
                      )}
                    </button>
                  </div>
                  <textarea
                    id="key_achievements"
                    name="key_achievements"
                    required
                    value={formData.key_achievements}
                    onChange={handleChange}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., 95% of our graduates met kindergarten readiness benchmarks, we serve 30% low-income families, awarded 'Excellence in Early Learning' by the state..."
                  />
                  <p className="text-xs text-gray-500 mt-1">This helps the AI showcase your credibility and track record</p>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label htmlFor="specific_needs" className="block text-sm font-medium text-gray-700">
                      What specific challenges or gaps will this grant help address? *
                    </label>
                    <button
                      type="button"
                      onClick={() => handleAutoGenerate('specific_needs')}
                      disabled={generatingField === 'specific_needs'}
                      className="flex items-center gap-1 px-3 py-1 text-xs bg-primary-50 text-primary-700 border border-primary-300 rounded-md hover:bg-primary-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {generatingField === 'specific_needs' ? (
                        <>
                          <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-primary-700"></div>
                          Generating...
                        </>
                      ) : (
                        <>
                          <Wand2 className="w-3 h-3" />
                          Auto-Generate
                        </>
                      )}
                    </button>
                  </div>
                  <textarea
                    id="specific_needs"
                    name="specific_needs"
                    required
                    value={formData.specific_needs}
                    onChange={handleChange}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., We have a 20-family waitlist, our playground equipment is outdated, we need to hire bilingual staff to serve Spanish-speaking families..."
                  />
                  <p className="text-xs text-gray-500 mt-1">This creates a compelling statement of need</p>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label htmlFor="target_outcomes" className="block text-sm font-medium text-gray-700">
                      What measurable outcomes do you hope to achieve with this grant? *
                    </label>
                    <button
                      type="button"
                      onClick={() => handleAutoGenerate('target_outcomes')}
                      disabled={generatingField === 'target_outcomes'}
                      className="flex items-center gap-1 px-3 py-1 text-xs bg-primary-50 text-primary-700 border border-primary-300 rounded-md hover:bg-primary-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {generatingField === 'target_outcomes' ? (
                        <>
                          <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-primary-700"></div>
                          Generating...
                        </>
                      ) : (
                        <>
                          <Wand2 className="w-3 h-3" />
                          Auto-Generate
                        </>
                      )}
                    </button>
                  </div>
                  <textarea
                    id="target_outcomes"
                    name="target_outcomes"
                    required
                    value={formData.target_outcomes}
                    onChange={handleChange}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., Serve 15 additional children, improve literacy scores by 20%, hire 2 new certified teachers, achieve QRIS Level 4 rating..."
                  />
                  <p className="text-xs text-gray-500 mt-1">This helps create specific, measurable outcomes sections</p>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label htmlFor="community_impact" className="block text-sm font-medium text-gray-700">
                      How does your organization impact the local community? *
                    </label>
                    <button
                      type="button"
                      onClick={() => handleAutoGenerate('community_impact')}
                      disabled={generatingField === 'community_impact'}
                      className="flex items-center gap-1 px-3 py-1 text-xs bg-primary-50 text-primary-700 border border-primary-300 rounded-md hover:bg-primary-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {generatingField === 'community_impact' ? (
                        <>
                          <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-primary-700"></div>
                          Generating...
                        </>
                      ) : (
                        <>
                          <Wand2 className="w-3 h-3" />
                          Auto-Generate
                        </>
                      )}
                    </button>
                  </div>
                  <textarea
                    id="community_impact"
                    name="community_impact"
                    required
                    value={formData.community_impact}
                    onChange={handleChange}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., We're the only preschool in a 10-mile radius, 70% of parents report we enabled them to maintain employment, we partner with local schools for smooth kindergarten transitions..."
                  />
                  <p className="text-xs text-gray-500 mt-1">This demonstrates community value and sustainability</p>
                </div>
              </div>
            </div>

            <div className="bg-accent-50 border-2 border-accent-400 rounded-lg p-4">
              <h3 className="text-sm font-display font-semibold text-primary-700 mb-2">What happens next?</h3>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Our AI will analyze the grant requirements and your responses</li>
                <li>• Generate 7 professional sections tailored to your organization</li>
                <li>• You can review, edit, and refine each section</li>
                <li>• Export to PDF when ready to submit</li>
              </ul>
            </div>

            <div className="flex gap-4">
              <button
                type="button"
                onClick={() => navigate('/grants')}
                className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 font-medium transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 px-6 py-3 bg-primary-500 text-white rounded-md hover:bg-primary-700 font-medium disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm transition-all hover:shadow-md"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Generating Application...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Generate Application
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
}
