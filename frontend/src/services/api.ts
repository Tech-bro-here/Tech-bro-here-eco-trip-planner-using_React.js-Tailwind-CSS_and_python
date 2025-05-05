import axios from 'axios';
import type { User, Review, HeatmapResponse } from '../types';

// Configure axios to include credentials
axios.defaults.withCredentials = true;

export interface ScrapeRequest {
  city: string;
  category: string;
}

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add a response interceptor to handle errors
api.interceptors.response.use(
  response => response,
  error => {
    // Handle errors here if needed
    return Promise.reject(error);
  }
);

const auth = {
  register: async (username: string, email: string, password: string): Promise<{ user: User }> => {
    const response = await api.post('/auth/register', { username, email, password });
    return response.data;
  },
  
  login: async (username: string, password: string): Promise<{ user: User }> => {
    const response = await api.post('/auth/login', { username, password });
    return response.data;
  },
  
  logout: async (): Promise<void> => {
    await api.post('/auth/logout');
  },
  
  me: async (): Promise<{ user: User }> => {
    const response = await api.get('/auth/me');
    return response.data;
  }
};

const apiService = {
  auth,

  scrape: async ({ city, category }: ScrapeRequest) => {
    const response = await api.post('/scrape', { city, category });
    return response.data;
  },

  processReviews: async () => {
    const response = await api.post('/process');
    return response.data;
  },

  getHeatmap: async (emotion: string): Promise<HeatmapResponse> => {
    const response = await api.get('/heatmap', {
      params: { emotion },
    });
    return response.data;
  },

  getReviews: async (location: string): Promise<{ reviews: Review[] }> => {
    const response = await api.get('/reviews', {
      params: { location },
    });
    return response.data;
  },

  itineraries: {
    getAll: async () => {
      const response = await api.get('/itineraries');
      return response.data;
    },

    create: async (hotspotIds: string[]) => {
      const response = await api.post('/itineraries', {
        hotspot_ids: hotspotIds,
      });
      return response.data;
    }
  }
};

export default apiService; 