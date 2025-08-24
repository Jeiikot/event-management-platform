import axios from 'axios';
import { parseError } from '../utils/errorHandler';

const client = axios.create({
  baseURL: import.meta?.env?.VITE_API_BASE_URL || process.env.VITE_API_BASE_URL || 'http://localhost:8000',
});

client.interceptors.request.use((config) => {
  const token = (typeof localStorage !== 'undefined') ? localStorage.getItem('token') : null;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

client.interceptors.response.use(
  (response) => response,
  (error) => Promise.reject(new Error(parseError(error)))
);

export default client;
