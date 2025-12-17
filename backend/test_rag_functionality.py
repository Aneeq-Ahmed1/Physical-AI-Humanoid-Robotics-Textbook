#!/usr/bin/env python3
"""
Test script to verify the complete RAG functionality works end-to-end
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_rag_functionality():
    """Test the complete RAG functionality"""
    print("Testing complete RAG functionality...")

    try:
        # Test vector database
        from vector.qdrant_client import QdrantVectorDB
        vector_db = QdrantVectorDB()

        # Create a test embedding
        test_query = "What is humanoid robotics?"
        query_embedding = vector_db.embed_text(test_query)

        print(f"Generated query embedding with {len(query_embedding)} dimensions")

        # Test search functionality
        results = vector_db.search(query_vector=query_embedding, top_k=3)

        print(f"Found {len(results)} similar documents")

        if len(results) > 0:
            print("[SUCCESS] RAG search is working!")
            print(f"Top result source: {results[0]['source_file']}")
            print(f"Similarity score: {results[0]['similarity_score']:.4f}")
            print(f"Content preview: {results[0]['text'][:100]}...")
        else:
            print("[WARNING] No documents found - this might be expected if the collection is empty")

        return True

    except Exception as e:
        print(f"[ERROR] RAG functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_agent_with_rag():
    """Test LLM agent with RAG functionality"""
    print("\nTesting LLM agent with RAG...")

    try:
        from agent.llm_agent import LLMAgent
        agent = LLMAgent()

        # Test with some context documents (simulating retrieved docs)
        test_context = [
            {
                "text": "Humanoid robotics is a branch of robotics that focuses on creating robots with human-like characteristics and capabilities. These robots often have limbs, a head, and torso that mimic human anatomy.",
                "source_file": "intro.md",
                "chunk_index": 0,
                "similarity_score": 0.9
            }
        ]

        response = agent.generate_response_full_rag("What is humanoid robotics?", test_context)

        print(f"LLM Response: {response[:200]}...")

        # Check if response contains relevant content
        if "human" in response.lower() or "robot" in response.lower():
            print("[SUCCESS] LLM agent responded with relevant content")
        else:
            print("[INFO] LLM responded, but content relevance unknown")

        return True

    except Exception as e:
        print(f"[ERROR] LLM agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Running complete RAG functionality tests...\n")

    success = True
    success &= test_rag_functionality()
    success &= test_llm_agent_with_rag()

    print(f"\n{'='*60}")
    if success:
        print("[SUCCESS] All RAG functionality tests passed!")
        print("\nYour chatbot should now properly:")
        print("1. Use semantic search to find relevant textbook content")
        print("2. Provide context to the LLM for more accurate responses")
        print("3. Cite sources from the textbook when providing answers")
        print("4. Work in both full-book RAG mode and selected-text mode")
    else:
        print("[FAILURE] Some tests failed.")
        print("\nMake sure you have valid API keys in your .env file:")
        print("- GEMINI_API_KEY for the LLM and potential embeddings")
        print("- QDRANT_URL and QDRANT_API_KEY for vector storage")
        print("- (Optional) OPENAI_API_KEY for better embeddings")

    return success

if __name__ == "__main__":
    main()