
#!/usr/bin/env python3
"""
Script to reindex all documents with the new embedding system
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.scripts.index_documents import create_document_chunks, index_documents_to_qdrant

def main():
    """
    Main function to run the indexing process from project root.
    """
    # Path to the Docusaurus docs directory from project root
    docs_dir = os.path.join(os.path.dirname(__file__), "my-website", "docs")

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

    print("Reindexing completed successfully!")

if __name__ == "__main__":
    main()