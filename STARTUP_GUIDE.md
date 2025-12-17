# Startup Guide for Humanoid Robotics RAG Chatbot

## Backend Server Setup

### Starting the Backend Server

From the `backend` directory, run one of these commands:

**Option 1: Direct uvicorn command**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option 2: Using Python module**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: If the above doesn't work due to import issues**
```bash
cd backend
PYTHONPATH=. uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables

Make sure to set up your `.env` file in the `backend` directory:

```bash
# .env file in backend directory
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```

## Frontend Setup

### Starting the Docusaurus Frontend

From the `my-website` directory:

```bash
cd my-website
npm install  # Only needed the first time
npm run start
```

### Environment Configuration for Frontend

If you're running the backend on a different port or server, you can configure it using an environment variable:

```bash
# Set environment variable before starting the frontend
export CHATBOT_API_URL=http://your-backend-url:8000
npm run start
```

On Windows Command Prompt:
```cmd
set CHATBOT_API_URL=http://your-backend-url:8000 && npm run start
```

The frontend will automatically use the configured API URL or default to `http://localhost:8000`.

## Common Issues and Solutions

### Issue 1: "Error loading ASGI app. Could not import module 'main'"
**Solution:** Run the server from the correct directory with the proper command:
```bash
cd backend
PYTHONPATH=. uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Issue 2: Frontend can't connect to backend
**Solution:** Make sure the backend server is running and the API URL is correctly configured in the frontend.

### Issue 3: Cohere API errors
**Solution:** Ensure your `COHERE_API_KEY` is valid and properly set in the `.env` file.

### Issue 4: Qdrant connection errors
**Solution:** Make sure your Qdrant database is set up with the correct collection name (`book-content`).

## Testing the System

### Backend Testing
1. Start the backend server
2. Visit `http://localhost:8000/health` to verify the server is running
3. The response should be: `{"status": "healthy", "timestamp": "..."}`

### Frontend Testing
1. Start both backend and frontend servers
2. Open the Docusaurus site in your browser
3. The chat widget should appear in the bottom-right corner
4. You should be able to send messages and receive responses

## Deployment Notes

### For Development
- Backend: Run with `--reload` flag for auto-reload on changes
- Frontend: Run with `npm run start` for development server

### For Production
- Backend: Use a production ASGI server like gunicorn
- Frontend: Build with `npm run build` and serve the static files