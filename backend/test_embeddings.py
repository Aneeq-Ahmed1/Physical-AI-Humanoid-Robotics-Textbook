#!/usr/bin/env python3
"""
Test script to verify the embedding functionality with the new OpenAI-based approach
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_embeddings():
    """Test the embedding functionality"""
    print("Testing embedding functionality...")

    try:
        from vector.qdrant_client import QdrantVectorDB

        # Create vector DB instance
        vector_db = QdrantVectorDB()

        # Test embedding a sample text
        sample_text = "This is a test about humanoid robotics and artificial intelligence."
        print(f"Embedding sample text: '{sample_text[:50]}...'")

        embedding = vector_db.embed_text(sample_text)

        print(f"Generated embedding with {len(embedding)} dimensions")
        print(f"First 10 dimensions: {embedding[:10]}")

        if len(embedding) == 1536:  # OpenAI embedding size
            print("[SUCCESS] Embedding has correct dimensions (1536)")
        else:
            print(f"[WARNING] Embedding has {len(embedding)} dimensions, expected 1536")

        # Test multiple embeddings
        sample_texts = [
            "Humanoid robotics is fascinating.",
            "Artificial intelligence helps robots understand.",
            "Machine learning enables robot adaptation."
        ]

        print("\nTesting multiple embeddings...")
        embeddings = vector_db.embed_documents(sample_texts)

        print(f"Generated {len(embeddings)} embeddings")
        if len(embeddings) == 3:
            print("[SUCCESS] Correct number of embeddings generated")
        else:
            print(f"[ERROR] Expected 3 embeddings, got {len(embeddings)}")

        # Test collection setup
        print(f"\nCollection '{vector_db.collection_name}' is ready for use")

        return True

    except Exception as e:
        print(f"[ERROR] Embedding test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_qdrant_connection():
    """Test Qdrant connection"""
    print("\nTesting Qdrant connection...")

    try:
        from vector.qdrant_client import QdrantVectorDB

        vector_db = QdrantVectorDB()

        # Try to get collection info
        collection_info = vector_db.client.get_collection(vector_db.collection_name)
        print(f"[SUCCESS] Connected to Qdrant collection: {vector_db.collection_name}")
        print(f"Collection vector size: {collection_info.config.params.vectors.size}")

        return True

    except Exception as e:
        print(f"[ERROR] Qdrant connection test failed: {e}")
        return False

def main():
    print("Running embedding functionality tests...\n")

    success = True
    success &= test_embeddings()
    success &= test_qdrant_connection()

    print(f"\n{'='*60}")
    if success:
        print("[SUCCESS] All embedding tests passed!")
        print("\nThe RAG functionality should now work properly with semantic search.")
        print("Documents will be indexed with proper semantic embeddings instead of hash-based ones.")
    else:
        print("[FAILURE] Some tests failed.")
        print("\nNote: If OpenAI API key is not available, the system will fall back to Gemini embeddings.")
        print("Make sure you have either an OpenAI API key or a valid GEMINI_API_KEY in your .env file.")

    return success

if __name__ == "__main__":
    main()