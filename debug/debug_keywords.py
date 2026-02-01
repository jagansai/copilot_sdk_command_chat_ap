"""Debug why 'how to view sessions' doesn't match 'Session list'"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag_engine import RAGEngine

# Load and initialize
commands_file = Path(__file__).parent.parent / "resources" / "commands.md"
commands = commands_file.read_text(encoding='utf-8')
rag = RAGEngine(commands, max_chunks=3)

# The problematic query
query = "how to view sessions"

print(f"Query: '{query}'")
print("="*60)

# Extract keywords from query
query_keywords = rag._extract_keywords(query)
print(f"\nQuery keywords: {query_keywords}")

# Check each chunk's keywords and score
print("\n\nChunk Analysis:")
print("-"*60)

for chunk in rag.chunks:
    score = rag._calculate_relevance_score(query_keywords, chunk)
    print(f"\nChunk: {chunk.title}")
    print(f"  Keywords: {chunk.keywords[:10]}...")  # First 10
    print(f"  Score: {score:.3f}")
    
    # Show which query keywords matched
    matches = [kw for kw in query_keywords if kw in chunk.keywords]
    print(f"  Matched: {matches}")

# Show what gets retrieved
print("\n\n" + "="*60)
print("Retrieved chunks:")
retrieved = rag.retrieve_relevant_chunks(query)
for chunk in retrieved:
    print(f"  - {chunk.title}")
