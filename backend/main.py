from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat import chat_router
from api.health import health_router
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Humanoid Robotics RAG Chatbot API",
    description="An agentic RAG chatbot for the Humanoid Robotics textbook",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from vector.qdrant_client import QdrantVectorDB
import os
from pathlib import Path

def check_and_index_documents():
    """Check if Qdrant collection has documents, and if not, index from docs directory"""
    try:
        vector_db = QdrantVectorDB()

        # Check if collection exists and has documents
        try:
            collection_info = vector_db.client.get_collection(vector_db.collection_name)
            if collection_info.points_count > 0:
                logger.info(f"Found {collection_info.points_count} documents in Qdrant collection '{vector_db.collection_name}'")
                return
        except:
            logger.info(f"Collection '{vector_db.collection_name}' does not exist, will create and populate it")

        logger.info("No documents found in Qdrant. Indexing documentation from Docusaurus site...")

        # Import and run indexing
        from scripts.index_documents import create_document_chunks, index_documents_to_qdrant
        docs_dir = os.path.join(os.path.dirname(__file__), "..", "my-website", "docs")
        docs_dir = os.path.abspath(docs_dir)

        if os.path.exists(docs_dir):
            documents = create_document_chunks(docs_dir)
            if documents:
                logger.info(f"Found {len(documents)} document chunks to index")
                index_documents_to_qdrant(documents)
                logger.info("Document indexing completed successfully!")
            else:
                logger.warning("No documents found to index from docs directory")
        else:
            logger.warning(f"Docs directory does not exist: {docs_dir}")

    except Exception as e:
        logger.error(f"Error during document indexing: {e}")

# Event handler for when the application starts
@app.on_event("startup")
def startup_event():
    logger.info("Starting up the application...")
    check_and_index_documents()
    logger.info("Application startup completed")

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(health_router, tags=["health"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)