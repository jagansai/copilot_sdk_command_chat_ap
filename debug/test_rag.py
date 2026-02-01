"""
Test script to demonstrate RAG engine functionality
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag_engine import RAGEngine

# Load the commands file
commands_file = Path(__file__).parent.parent / "resources" / "commands.md"
commands = commands_file.read_text(encoding='utf-8')

# Initialize RAG engine
rag = RAGEngine(commands, max_chunks=3)

# Get stats
stats = rag.get_stats()
print("=== RAG Engine Stats ===")
print(f"Total chunks: {stats['total_chunks']}")
print(f"Max chunks per query: {stats['max_chunks_per_query']}")
print("\nAvailable commands:")
for title in stats['chunk_titles']:
    print(f"  - {title}")

# Test queries
print("\n\n=== Testing RAG Retrieval ===\n")

test_queries = [
    "How do I list sessions?",
    "How to delete a user?",
    "Show me exchange information",
    "What markets are available?"
]

for query in test_queries:
    print(f"\nQuery: '{query}'")
    print("-" * 50)
    relevant_chunks = rag.retrieve_relevant_chunks(query)
    print(f"Retrieved {len(relevant_chunks)} relevant chunks:")
    for chunk in relevant_chunks:
        print(f"  → {chunk.title}")
    print()
