from ..skill_registry import register_skill
from typing import List, Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


@register_skill(
    skill_id="retrieve_book_chunks",
    name="Retrieve Book Chunks",
    description="Retrieve relevant chunks of text from the book based on the query using RAG techniques",
    input_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The query to search for in the book"},
            "max_chunks": {"type": "integer", "description": "Maximum number of chunks to return", "default": 5}
        },
        "required": ["query"]
    },
    output_schema={
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The content of the chunk"},
                "source": {"type": "string", "description": "Source of the chunk (e.g., chapter, section)"},
                "similarity_score": {"type": "number", "description": "Similarity score of the chunk to the query"}
            }
        }
    }
)
def retrieve_book_chunks(query: str, max_chunks: int = 5, **kwargs) -> List[Dict[str, Any]]:
    """Retrieve relevant chunks of text from the book based on the query.

    Args:
        query: The query to search for in the book
        max_chunks: Maximum number of chunks to return (default: 5)
        **kwargs: Additional parameters

    Returns:
        List of chunks with content, source, and similarity information
    """
    try:
        # Connect to the vector database and perform RAG search
        from ...vector.qdrant_client import QdrantVectorDB

        vector_db = QdrantVectorDB()

        # Create embedding for the query
        query_embedding = vector_db.embed_text(query)

        # Retrieve relevant documents from Qdrant
        retrieved_docs = vector_db.search(query_vector=query_embedding, top_k=max_chunks)

        # Format the results to match the expected schema
        chunks = []
        for doc in retrieved_docs:
            chunks.append({
                "content": doc["text"],
                "source": doc["source_file"],
                "similarity_score": doc["similarity_score"]
            })

        return chunks

    except Exception as e:
        logger.error(f"Error in retrieve_book_chunks skill: {e}")
        # Return empty list if there's an error
        return []


@register_skill(
    skill_id="search_book_content",
    name="Search Book Content",
    description="Search the book content using keyword and semantic search techniques",
    input_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query"},
            "search_type": {"type": "string", "enum": ["keyword", "semantic", "hybrid"], "default": "semantic"},
            "max_results": {"type": "integer", "description": "Maximum number of results to return", "default": 10}
        },
        "required": ["query"]
    },
    output_schema={
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The content of the search result"},
                "source": {"type": "string", "description": "Source of the content"},
                "score": {"type": "number", "description": "Relevance score of the result"}
            }
        }
    }
)
def search_book_content(query: str, search_type: str = "semantic", max_results: int = 10, **kwargs) -> List[Dict[str, Any]]:
    """Search the book content using various search techniques.

    Args:
        query: The search query
        search_type: Type of search to perform (keyword, semantic, hybrid)
        max_results: Maximum number of results to return (default: 10)
        **kwargs: Additional parameters

    Returns:
        List of search results with content, source, and relevance score
    """
    try:
        # Connect to the vector database and perform RAG search
        from ...vector.qdrant_client import QdrantVectorDB

        vector_db = QdrantVectorDB()

        # Create embedding for the query
        query_embedding = vector_db.embed_text(query)

        # Retrieve relevant documents from Qdrant
        retrieved_docs = vector_db.search(query_vector=query_embedding, top_k=max_results)

        # Format the results to match the expected schema
        results = []
        for doc in retrieved_docs:
            results.append({
                "content": doc["text"],
                "source": doc["source_file"],
                "score": doc["similarity_score"]
            })

        return results
    except Exception as e:
        logger.error(f"Error in search_book_content skill: {e}")
        return []


@register_skill(
    skill_id="get_book_outline",
    name="Get Book Outline",
    description="Retrieve the outline or table of contents of the book",
    input_schema={
        "type": "object",
        "properties": {}
    },
    output_schema={
        "type": "object",
        "properties": {
            "outline": {"type": "array", "items": {"type": "string"}}
        }
    }
)
def get_book_outline(**kwargs) -> Dict[str, Any]:
    """Retrieve the outline or table of contents of the book.

    Args:
        **kwargs: Additional parameters

    Returns:
        Dictionary containing the book outline
    """
    try:
        # This would connect to the actual book metadata in a real implementation
        # For now, return a simulated outline
        return {
            "outline": [
                "Chapter 1: Introduction to Humanoid Robotics",
                "Chapter 2: Biomechanics and Movement",
                "Chapter 3: Perception Systems",
                "Chapter 4: Control Systems",
                "Chapter 5: Learning and Adaptation",
                "Chapter 6: Human-Robot Interaction"
            ]
        }
    except Exception as e:
        logger.error(f"Error in get_book_outline skill: {e}")
        return {"outline": []}