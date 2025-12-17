# Setting Up the Humanoid Robotics Chatbot with Gemini API

This guide explains how to set up the chatbot to work with Google's Gemini API via OpenAI SDK.

## Prerequisites

1. **Google AI Studio Account**: Create an account at [Google AI Studio](https://aistudio.google.com/)
2. **Gemini API Key**: Generate an API key from Google AI Studio
3. **Python Environment**: Make sure Python 3.8+ is installed
4. **Node.js**: For the Docusaurus frontend

## Step-by-Step Setup

### 1. Backend Configuration

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the `.env` file with your actual Gemini API key:
   ```env
   # Replace YOUR_GEMINI_API_KEY_HERE with your actual API key from Google AI Studio
   GEMINI_API_KEY="your-actual-api-key-here"
   ```

4. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

   The backend will start on `http://localhost:8000`

### 2. Frontend Setup

1. Navigate to the Docusaurus website directory:
   ```bash
   cd my-website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run start
   ```

### 3. How It Works

- The backend uses a custom wrapper (`agent/gemini_openai_wrapper.py`) to make Gemini API calls compatible with OpenAI SDK format
- The frontend automatically connects to `http://localhost:8000/api/chat` by default
- Two modes are supported:
  - **Full-book RAG Mode**: Answers based on the entire textbook content
  - **Selected-text Mode**: Answers based only on user-selected text

### 4. Troubleshooting

**Issue**: "Sorry, I encountered an error while processing your request"
**Solution**:
- Verify your GEMINI_API_KEY is valid
- Check that the backend is running on `http://localhost:8000`
- Look at backend console for specific error messages

**Issue**: Backend won't start
**Solution**:
- Ensure all dependencies are installed
- Check that environment variables are properly set
- Verify Qdrant connection if using RAG mode

### 5. Testing the Setup

1. Once both backend and frontend are running:
   - Backend: `http://localhost:8000` (should show API docs)
   - Frontend: `http://localhost:3000` (your Docusaurus site)

2. Use the chat widget on the frontend to test responses

## Architecture Notes

- The system uses a custom `OpenAIGeminiClient` wrapper that translates OpenAI SDK calls to Gemini API calls
- Document indexing happens automatically on startup if no documents exist in Qdrant
- Session management maintains conversation history with 24-hour expiration
- CORS is configured to allow all origins during development

## Security Notes

- Never commit your actual API key to version control
- Use environment variables for all sensitive information
- The current setup uses `"*"` for CORS origins - restrict this in production

## Getting Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key"
4. Create a new API key or use an existing one
5. Copy the key and add it to your `.env` file

Your chatbot should now be fully functional with Google's Gemini API!