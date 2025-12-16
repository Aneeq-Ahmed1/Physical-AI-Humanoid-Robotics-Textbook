#!/usr/bin/env python3
"""
Script to index documentation content from Docusaurus site into Qdrant vector database.
This script reads markdown files from the Docusaurus docs directory and indexes them
into the Qdrant collection for RAG functionality.
"""
import os
import re
from typing import List, Dict, Any
import asyncio
from pathlib import Path
import hashlib

# Add the backend directory to the path so we can import our modules
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vector.qdrant_client import QdrantVectorDB
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_markdown(file_path: str) -> str:
    """
    Extract plain text content from a markdown file, removing markdown syntax.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove markdown headers but keep the text
    content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)

    # Remove other markdown elements but preserve the text
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
    content = re.sub(r'\*(.*?)\*', r'\1', content)      # Italic
    content = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', content)  # Links
    content = re.sub(r'`([^`]+)`', r'\1', content)      # Code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)  # Code fences

    # Remove image references
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)

    # Clean up multiple newlines
    content = re.sub(r'\n\s*\n', '\n\n', content)

    return content.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks for better retrieval.
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If we're near the end, include the rest
        if end >= len(text):
            chunks.append(text[start:])
            break

        # Find a good break point (try to break at sentence or paragraph boundaries)
        chunk = text[start:end]

        # Look for a good break point if we're in the middle of a sentence
        if end < len(text):
            # Look for a sentence end in the last 100 characters
            last_period = chunk.rfind('.', end - 100, end)
            if last_period != -1:
                end = start + last_period + 1
            else:
                # Look for a newline
                last_newline = chunk.rfind('\n', end - 100, end)
                if last_newline != -1:
                    end = start + last_newline + 1

        chunks.append(text[start:end])
        start = end - overlap  # Overlap to preserve context

        # If overlap would cause us to go backwards, advance by chunk_size
        if start >= end:
            start = end

    # Remove any empty chunks
    chunks = [chunk for chunk in chunks if chunk.strip()]

    return chunks

def create_document_chunks(docs_dir: str) -> List[Dict[str, Any]]:
    """
    Read all markdown files from the docs directory and create document chunks.
    """
    documents = []
    docs_path = Path(docs_dir)

    # Find all markdown files in the docs directory
    for md_file in docs_path.rglob("*.md"):
        if md_file.name.startswith('.'):  # Skip hidden files
            continue

        relative_path = md_file.relative_to(docs_path.parent if docs_path.parent.name == 'my-website' else docs_path)

        print(f"Processing: {relative_path}")

        try:
            content = extract_text_from_markdown(str(md_file))

            # Skip if content is too short
            if len(content.strip()) < 50:
                continue

            # Create chunks from the content
            chunks = chunk_text(content)

            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) < 20:  # Skip very small chunks
                    continue

                documents.append({
                    "text": chunk,
                    "source_file": str(relative_path),
                    "chunk_index": i,
                    "file_path": str(md_file)
                })
        except Exception as e:
            print(f"Error processing {relative_path}: {e}")
            continue

    return documents

def index_documents_to_qdrant(documents: List[Dict[str, Any]]):
    """
    Index documents to Qdrant using the existing vector database client.
    """
    print(f"Indexing {len(documents)} document chunks to Qdrant...")

    # Use the existing Qdrant client
    vector_db = QdrantVectorDB()

    points = []

    for i, doc in enumerate(documents):
        # Create embedding for the text
        embedding = vector_db.embed_text(doc["text"])

        # Create a unique ID for this document chunk
        text_hash = hashlib.md5(f"{doc['text']}_{doc['chunk_index']}".encode()).hexdigest()

        # Create the point for Qdrant
        point = {
            "id": text_hash,
            "vector": embedding,
            "payload": {
                "text": doc["text"],
                "source_file": doc["source_file"],
                "chunk_index": doc["chunk_index"]
            }
        }

        points.append(point)

        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{len(documents)} documents...")

    # Upload points to Qdrant
    try:
        from qdrant_client.http import models
        from qdrant_client.http.models import PointStruct

        # Prepare PointStruct objects
        point_structs = []
        for point in points:
            point_structs.append(PointStruct(
                id=point["id"],
                vector=point["vector"],
                payload=point["payload"]
            ))

        # Upload to Qdrant
        vector_db.client.upsert(
            collection_name=vector_db.collection_name,
            points=point_structs
        )

        print(f"Successfully indexed {len(point_structs)} documents to Qdrant!")

    except Exception as e:
        print(f"Error indexing to Qdrant: {e}")
        raise

def main():
    """
    Main function to run the indexing process.
    """
    # Path to the Docusaurus docs directory
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "my-website", "docs")

    if not os.path.exists(docs_dir):
        print(f"Docs directory not found: {docs_dir}")
        return

    print(f"Reading documentation from: {docs_dir}")

    # Create document chunks
    documents = create_document_chunks(docs_dir)

    if not documents:
        print("No documents found to index!")
        return

    print(f"Found {len(documents)} document chunks to index")

    # Index to Qdrant
    index_documents_to_qdrant(documents)

    print("Indexing completed successfully!")

if __name__ == "__main__":
    main()