import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { applicationAPI } from '../../services/api';
import { ArrowLeft, Edit2, Save, X, FileText, Download } from 'lucide-react';
import Layout from '../common/Layout';

export default function ApplicationViewer() {
  const { applicationId } = useParams();
  const navigate = useNavigate();
  const [application, setApplication] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingSection, setEditingSection] = useState(null);
  const [editedContent, setEditedContent] = useState('');
  const [saving, setSaving] = useState(false);

  const sectionTitles = {
    executive_summary: 'Executive Summary',
    organizational_background: 'Organizational Background',
    need_statement: 'Statement of Need',
    project_description: 'Project Description',
    expected_outcomes: 'Expected Outcomes',
    budget_justification: 'Budget Justification',
    sustainability_plan: 'Sustainability Plan'
  };

  useEffect(() => {
    fetchApplication();
  }, [applicationId]);

  const fetchApplication = async () => {
    try {
      setLoading(true);
      const response = await applicationAPI.get(applicationId);
      setApplication(response.data);
    } catch (err) {
      setError('Failed to load application. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEditClick = (sectionName, content) => {
    setEditingSection(sectionName);
    setEditedContent(content);
  };

  const handleCancelEdit = () => {
    setEditingSection(null);
    setEditedContent('');
  };

  const handleSaveEdit = async () => {
    setSaving(true);
    try {
      const updatedSections = {
        ...application.sections,
        [editingSection]: editedContent
      };

      const response = await applicationAPI.update(applicationId, updatedSections);
      setApplication(response.data);
      setEditingSection(null);
      setEditedContent('');
    } catch (err) {
      alert('Failed to save changes. Please try again.');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-[50vh]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading application...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error || !application) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-[50vh]">
          <div className="text-center">
            <p className="text-red-600">{error || 'Application not found'}</p>
            <button
              onClick={() => navigate('/grants')}
              className="mt-4 px-4 py-2 bg-primary-500 text-white rounded-md hover:bg-primary-700"
            >
              Back to Grants
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <button
          onClick={() => navigate('/grants')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Grants
        </button>

        <div className="bg-white rounded-lg shadow-md p-8 mb-6">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h1 className="text-3xl font-display font-bold text-gray-900 mb-2 tracking-tight">{application.grant_title}</h1>
              <div className="flex items-center gap-3 text-sm text-gray-600">
                <span className="px-3 py-1 bg-accent-100 text-primary-700 border border-accent-400 rounded-full font-medium">
                  {application.status.charAt(0).toUpperCase() + application.status.slice(1)}
                </span>
                <span>Created {new Date(application.created_at).toLocaleDateString()}</span>
              </div>
            </div>
            <button
              onClick={() => alert('PDF export coming soon!')}
              className="flex items-center gap-2 px-4 py-2 bg-accent-400 text-gray-900 rounded-md hover:bg-accent-500 font-medium shadow-sm transition-all hover:shadow-md"
            >
              <Download className="w-4 h-4" />
              Export PDF
            </button>
          </div>

          <div className="bg-primary-50 border-2 border-primary-200 rounded-lg p-4 mb-6">
            <div className="flex items-start gap-3">
              <FileText className="w-5 h-5 text-primary-600 mt-0.5" />
              <div>
                <h3 className="text-sm font-display font-semibold text-primary-700">Your Grant Application</h3>
                <p className="text-sm text-gray-700 mt-1">
                  Review each section below. Click the edit button to make changes to any section.
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-8">
            {Object.entries(application.sections).map(([sectionName, content]) => (
              <div key={sectionName} className="border-b border-gray-200 pb-6 last:border-b-0">
                <div className="flex items-center justify-between mb-3">
                  <h2 className="text-xl font-display font-bold text-gray-900 tracking-tight">
                    {sectionTitles[sectionName] || sectionName}
                  </h2>
                  {editingSection === sectionName ? (
                    <div className="flex gap-2">
                      <button
                        onClick={handleSaveEdit}
                        disabled={saving}
                        className="flex items-center gap-1 px-3 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm disabled:bg-gray-400"
                      >
                        <Save className="w-4 h-4" />
                        {saving ? 'Saving...' : 'Save'}
                      </button>
                      <button
                        onClick={handleCancelEdit}
                        className="flex items-center gap-1 px-3 py-1 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 text-sm"
                      >
                        <X className="w-4 h-4" />
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={() => handleEditClick(sectionName, content)}
                      className="flex items-center gap-1 px-3 py-1 bg-primary-500 text-white rounded-md hover:bg-primary-700 text-sm shadow-sm transition-all"
                    >
                      <Edit2 className="w-4 h-4" />
                      Edit
                    </button>
                  )}
                </div>

                {editingSection === sectionName ? (
                  <textarea
                    value={editedContent}
                    onChange={(e) => setEditedContent(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 font-serif"
                    rows={12}
                  />
                ) : (
                  <div className="prose prose-lg max-w-none">
                    {content.split('\n\n').map((paragraph, idx) => (
                      <p key={idx} className="text-gray-700 leading-relaxed mb-4">
                        {paragraph}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
}
