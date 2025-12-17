// API configuration for the chatbot
// This can be overridden by environment variables during build time
const chatbotConfig = {
  apiUrl: typeof process !== 'undefined' ? (process.env.REACT_APP_API_URL || 'http://localhost:8000') : 'http://localhost:8000'
};

export default chatbotConfig;