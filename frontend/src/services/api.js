import axios from 'axios';
import { API_URL, API_TIMEOUT } from '../config';

const api = axios.create({
  baseURL: API_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and haven't retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token, refresh_token } = response.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

// Auth endpoints
export const authAPI = {
  register: (email, password) => api.post('/auth/register', { email, password }),
  login: (email, password) => api.post('/auth/login', { email, password }),
  getMe: () => api.get('/auth/me'),
};

// Profile endpoints
export const profileAPI = {
  get: () => api.get('/profile'),
  create: (data) => api.post('/profile', data),
  update: (data) => api.put('/profile', data),
};

// Grant endpoints
export const grantAPI = {
  list: (params) => api.get('/grants', { params }),
  get: (id) => api.get(`/grants/${id}`),
};

// Application endpoints
export const applicationAPI = {
  generate: (grantId, orgData) => api.post('/applications/generate', { grant_id: grantId, org_data: orgData }),
  list: (params) => api.get('/applications', { params }),
  get: (id) => api.get(`/applications/${id}`),
  refine: (id, sectionName, feedback) => api.post(`/applications/${id}/refine`, { section_name: sectionName, feedback }),
  update: (id, sections) => api.put(`/applications/${id}`, sections),
  delete: (id) => api.delete(`/applications/${id}`),
  getPersonalizationSuggestion: (fieldName, orgData) => api.post('/applications/personalization-suggestion', {
    field_name: fieldName,
    ...orgData
  }),
};
