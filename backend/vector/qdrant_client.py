import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()

class QdrantVectorDB:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        self.collection_name = "book-content"
        # Initialize OpenAI client for embeddings
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-"))  # Using placeholder if not set
        # Ensure the collection exists with proper vector size (OpenAI embeddings are 1536-dim)
        self._ensure_collection()

    def _ensure_collection(self):
        """
        Ensure the Qdrant collection exists with the correct vector size for our embedding model
        """
        try:
            # Check if collection exists
            collection_info = self.client.get_collection(self.collection_name)
            # If it exists, verify the vector size matches our embedding model
            expected_size = 1536  # OpenAI text-embedding-ada-002 produces 1536-dimensional vectors
            actual_size = collection_info.config.params.vectors.size

            if actual_size != expected_size:
                print(f"Warning: Collection vector size mismatch. Expected: {expected_size}, Actual: {actual_size}")
                print(f"Deleting existing collection '{self.collection_name}' to recreate with correct dimensions...")
                self.client.delete_collection(self.collection_name)
                print(f"Creating collection '{self.collection_name}' with {expected_size}-dimensional vectors...")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=expected_size, distance=Distance.COSINE)
                )
                print(f"Collection '{self.collection_name}' recreated successfully with correct dimensions!")
            else:
                print(f"Collection '{self.collection_name}' already exists with correct dimensions ({expected_size}).")
        except:
            # Collection doesn't exist, create it
            print(f"Creating collection '{self.collection_name}' with {expected_size}-dimensional vectors...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
            print(f"Collection '{self.collection_name}' created successfully!")

    def search(self, query_vector: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar documents in the vector database
        """
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )

            documents = []
            for result in search_results:
                documents.append({
                    "text": result.payload["text"],
                    "source_file": result.payload["source_file"],
                    "chunk_index": result.payload["chunk_index"],
                    "similarity_score": result.score
                })

            return documents
        except Exception as e:
            print(f"Error searching Qdrant: {e}")
            return []

    def embed_text(self, text: str) -> List[float]:
        """
        Create embeddings for text using OpenAI's embedding API
        """
        try:
            # Use OpenAI's embedding API
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"  # Using OpenAI's standard embedding model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating OpenAI embedding: {e}")
            print("Falling back to Gemini API for embeddings...")

            # Fallback to using Gemini API for embeddings (if available)
            try:
                import google.generativeai as genai
                api_key = os.getenv("GEMINI_API_KEY")
                if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
                    # Use Gemini's embedding functionality
                    genai.configure(api_key=api_key)
                    result = genai.embed_content(
                        model="models/embedding-001",
                        content=text,
                        task_type="retrieval_document"
                    )
                    embedding = result['embedding']
                    # Pad or truncate to 1536 if needed (though Gemini embeddings are typically 768)
                    while len(embedding) < 1536:
                        embedding.append(0.0)
                    embedding = embedding[:1536]
                    return embedding
            except Exception as gemini_error:
                print(f"Gemini embedding also failed: {gemini_error}")

            # Final fallback to improved hash-based embedding with semantic elements
            return self._semantic_hash_embedding(text)

    def _semantic_hash_embedding(self, text: str) -> List[float]:
        """
        Create a more semantic hash-based embedding by considering word frequencies and positions
        """
        import hashlib
        import re

        # Simple preprocessing
        words = re.findall(r'\b\w+\b', text.lower())

        # Create a more semantic representation
        embedding = [0.0] * 1536

        if not words:
            # If no words, return a simple hash-based embedding
            text_hash = hashlib.md5(text.encode()).hexdigest()
            for i in range(0, len(text_hash), 2):
                hex_pair = text_hash[i:i+2]
                if i // 2 < 1536:
                    embedding[i // 2] = int(hex_pair, 16) / 255.0
            return embedding

        # Create a frequency-based representation
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Use a simple approach to distribute word information across the embedding
        for i, word in enumerate(words):
            # Hash the word to get a position in the embedding space
            word_hash = hashlib.md5(word.encode()).hexdigest()
            # Use the hash to determine which positions to modify
            for j in range(0, len(word_hash), 4):  # Process in chunks of 4 hex chars
                if j // 2 < len(embedding):
                    hex_chunk = word_hash[j:j+4]
                    if hex_chunk:
                        # Convert hex chunk to a value between 0 and 1
                        val = int(hex_chunk, 16) / 65535.0  # 65535 = 0xFFFF
                        pos = (i * 100 + j // 4) % len(embedding)  # Distribute across embedding
                        embedding[pos] = (embedding[pos] + val) / 2  # Average with existing value

        return embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple documents using OpenAI's embedding API
        """
        try:
            # Generate embeddings using OpenAI API for all texts
            response = self.openai_client.embeddings.create(
                input=texts,
                model="text-embedding-ada-002"
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            print(f"Error generating OpenAI embeddings for multiple texts: {e}")
            # Fallback to calling embed_text individually (which has its own fallbacks)
            return [self.embed_text(text) for text in texts]