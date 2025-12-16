import os
import cohere
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv

load_dotenv()

class QdrantVectorDB:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        self.collection_name = "book-content"
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))

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
        Create embeddings for text using Cohere's embedding API
        """
        try:
            # Use Cohere's embed API to generate embeddings
            response = self.co.embed(
                texts=[text],
                model='embed-english-v3.0',
                input_type='search_query'  # or 'search_document' for documents
            )

            # Return the first embedding (we only embedded one text)
            return response.embeddings[0]
        except Exception as e:
            print(f"Error generating embedding: {e}")
            # Fallback to a simple hash-based embedding if API fails
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            embedding = []
            for i in range(0, len(text_hash), 2):
                hex_pair = text_hash[i:i+2]
                val = int(hex_pair, 16) / 255.0  # Normalize to 0-1
                embedding.append(val)

            # Pad or truncate to expected size (1024 for Cohere embeddings)
            while len(embedding) < 1024:
                embedding.append(0.0)
            embedding = embedding[:1024]

            return embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple documents using Cohere's embedding API
        """
        try:
            response = self.co.embed(
                texts=texts,
                model='embed-english-v3.0',
                input_type='search_document'
            )

            return response.embeddings
        except Exception as e:
            print(f"Error generating embeddings for documents: {e}")
            # Fallback to simple hash-based embeddings
            return [self.embed_text(text) for text in texts]