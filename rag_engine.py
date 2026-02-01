"""
RAG Engine for Command Chat Assistant

Handles document chunking, retrieval, and context injection
for efficient command documentation querying.
"""

import re
from dataclasses import dataclass


@dataclass
class CommandChunk:
    """Represents a single command documentation chunk."""
    title: str
    content: str
    keywords: list[str]
    
    def __str__(self) -> str:
        return f"{self.title}\n{self.content}"


class RAGEngine:
    """Retrieval-Augmented Generation engine for command documentation."""
    
    # Define synonyms for common command terms
    SYNONYMS = {
        'view': ['show', 'display', 'list', 'see', 'get'],
        'show': ['view', 'display', 'list', 'see', 'get'],
        'list': ['view', 'show', 'display', 'see', 'get'],
        'display': ['view', 'show', 'list', 'see', 'get'],
        'delete': ['remove', 'terminate', 'kill', 'end'],
        'remove': ['delete', 'terminate', 'kill', 'end'],
        'terminate': ['delete', 'remove', 'kill', 'end'],
        'create': ['add', 'new', 'make'],
        'add': ['create', 'new', 'make'],
    }
    
    def __init__(self, document: str, max_chunks: int = 3):
        """
        Initialize the RAG engine.
        
        Args:
            document: The full markdown documentation text
            max_chunks: Maximum number of chunks to retrieve per query
        """
        self.document = document
        self.max_chunks = max_chunks
        self.chunks: list[CommandChunk] = []
        self._chunk_document()
    
    def _chunk_document(self) -> None:
        """Split the document into logical command chunks."""
        # Remove markdown code fences if present
        doc = self.document.strip()
        if doc.startswith('```'):
            # Remove opening fence
            lines = doc.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            # Remove closing fence
            if lines and lines[-1].startswith('```'):
                lines = lines[:-1]
            doc = '\n'.join(lines)
        
        # Split by horizontal rules (---)
        sections = re.split(r'\n---+\n', doc)
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Skip Table of Contents and title sections
            # Check for ## followed by space or newline (not ###)
            if re.match(r'^##\s', section):
                continue
            
            # Extract command title (first line starting with ###)
            title_match = re.search(r'^###\s+(.+)$', section, re.MULTILINE)
            if not title_match:
                continue
            
            title = title_match.group(1).strip()
            
            # Extract keywords from title and content
            keywords = self._extract_keywords(section)
            
            chunk = CommandChunk(
                title=title,
                content=section,
                keywords=keywords
            )
            self.chunks.append(chunk)
    
    def _extract_keywords(self, text: str) -> list[str]:
        """Extract keywords from text for searching."""
        # Remove markdown formatting
        clean_text = re.sub(r'[#*`|]', '', text)
        
        # Extract words (alphanumeric + underscores)
        words = re.findall(r'\b\w+\b', clean_text.lower())
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                     'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
                     'are', 'been', 'be', 'have', 'has', 'had', 'do', 'does',
                     'this', 'that', 'these', 'those', 'it'}
        
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Add simple stemming: include both singular and plural forms
        expanded_keywords = set(keywords)
        for word in keywords:
            # If word ends in 's', add version without 's'
            if word.endswith('s') and len(word) > 3:
                expanded_keywords.add(word[:-1])
            # Add plural form for words that don't end in 's'
            elif not word.endswith('s'):
                expanded_keywords.add(word + 's')
        
        return list(expanded_keywords)
    
    def retrieve_relevant_chunks(self, query: str) -> list[CommandChunk]:
        """
        Retrieve the most relevant chunks for a given query.
        
        Args:
            query: User's question or search query
            
        Returns:
            List of relevant CommandChunk objects
        """
        query_keywords = self._extract_keywords(query)
        
        # Score each chunk based on keyword overlap
        scored_chunks: list[tuple[CommandChunk, float]] = []
        
        for chunk in self.chunks:
            score = self._calculate_relevance_score(query_keywords, chunk)
            if score > 0:
                scored_chunks.append((chunk, score))
        
        # Sort by score (descending) and take top N
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        top_chunks = [chunk for chunk, _ in scored_chunks[:self.max_chunks]]
        
        # If no matches, return all chunks as fallback
        if not top_chunks:
            return self.chunks[:self.max_chunks]
        
        return top_chunks
    
    def _calculate_relevance_score(self, query_keywords: list[str], 
                                   chunk: CommandChunk) -> float:
        """Calculate relevance score between query and chunk."""
        if not query_keywords:
            return 0.0
        
        # Extract title words for proper word matching (not substring)
        title_words = set(self._extract_keywords(chunk.title))
        
        # Count matches in content and title
        content_matches = self._count_content_matches(query_keywords, chunk.keywords)
        title_matches = self._count_title_matches(query_keywords, title_words)
        
        # Calculate score with higher weight for title matches
        content_score = content_matches / len(query_keywords)
        title_score = title_matches * 0.8  # Higher bonus for title matches
        
        return content_score + title_score
    
    def _count_content_matches(self, query_keywords: list[str], chunk_keywords: list[str]) -> float:
        """Count keyword matches in chunk content, including synonyms."""
        matches = 0.0
        
        for kw in query_keywords:
            # Direct match in content
            if kw in chunk_keywords:
                matches += 1
            # Check synonyms in content
            elif kw in self.SYNONYMS:
                if self._has_synonym_match(kw, chunk_keywords):
                    matches += 0.7  # Slightly lower score for synonym match
        
        return matches
    
    def _count_title_matches(self, query_keywords: list[str], title_words: set[str]) -> float:
        """Count keyword matches in title, including synonyms."""
        matches = 0.0
        
        for kw in query_keywords:
            # Direct match in title
            if kw in title_words:
                matches += 1
            # Check synonyms in title
            elif kw in self.SYNONYMS:
                if self._has_synonym_match(kw, title_words):
                    matches += 0.7  # Slightly lower for synonym
        
        return matches
    
    def _has_synonym_match(self, keyword: str, word_list: list[str] | set[str]) -> bool:
        """Check if any synonym of the keyword exists in the word list."""
        if keyword not in self.SYNONYMS:
            return False
        
        for syn in self.SYNONYMS[keyword]:
            if syn in word_list:
                return True
        return False
    
    def get_context_for_query(self, query: str) -> str:
        """
        Get formatted context string for a query.
        
        Args:
            query: User's question
            
        Returns:
            Formatted markdown context with relevant commands
        """
        relevant_chunks = self.retrieve_relevant_chunks(query)
        
        if not relevant_chunks:
            return "No relevant commands found."
        
        # Format chunks into context
        context_parts = [
            "Relevant Commands:\n",
            "\n---\n".join(str(chunk) for chunk in relevant_chunks)
        ]
        
        return "".join(context_parts)
    
    def get_stats(self) -> dict:
        """Get statistics about the chunked document."""
        return {
            "total_chunks": len(self.chunks),
            "chunk_titles": [chunk.title for chunk in self.chunks],
            "max_chunks_per_query": self.max_chunks
        }
