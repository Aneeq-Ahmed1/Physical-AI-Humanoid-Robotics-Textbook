// Chatbot configuration script
// This sets the global API URL for the chatbot component
// It can be overridden by setting CHATBOT_API_URL environment variable during build

(function() {
  // Set the default API URL
  window.CHATBOT_API_URL = window.CHATBOT_API_URL || 'http://localhost:8000';

  // For development, you can also check for a meta tag that might be injected during build
  const metaTag = document.querySelector('meta[name="chatbot-api-url"]');
  if (metaTag && metaTag.content) {
    window.CHATBOT_API_URL = metaTag.content;
  }

  console.log('Chatbot API URL configured to:', window.CHATBOT_API_URL);
})();