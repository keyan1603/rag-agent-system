"""
RAG Retriever Module

This module implements semantic search over the knowledge base using TF-IDF vectorization.

In production, you would replace this with:
- Pinecone (vector database)
- Weaviate (vector database)
- Milvus (vector database)
- Elasticsearch with dense_vector mapping
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any


class RAGRetriever:
    """
    Retriever for semantic search over knowledge base documents.
    
    Uses TF-IDF vectorization for efficient similarity search.
    """
    
    def __init__(self, knowledge_base: List[Dict[str, Any]]):
        """
        Initialize retriever with knowledge base documents.
        
        Args:
            knowledge_base: List of documents with 'id', 'title', and 'content'
        """
        self.documents = knowledge_base
        self.contents = [doc["content"] for doc in knowledge_base]
        
        # Create TF-IDF vectorizer for semantic search
        # max_features limits vocabulary size for efficiency
        # stop_words removes common words like 'the', 'and', etc.
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            lowercase=True,
            min_df=1,  # Include terms that appear in at least 1 document
            max_df=0.9  # Exclude terms that appear in > 90% of documents
        )
        
        # Fit vectorizer on all documents
        # This learns the vocabulary and term frequencies
        self.doc_vectors = self.vectorizer.fit_transform(self.contents)
        
        print(f"✓ RAGRetriever initialized with {len(self.documents)} documents")
        print(f"  Vocabulary size: {len(self.vectorizer.get_feature_names_out())}")
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve top-k most relevant documents for a query.
        
        The process:
        1. Convert query to TF-IDF vector
        2. Calculate cosine similarity with all document vectors
        3. Sort by similarity score
        4. Return top-k results above relevance threshold
        
        Args:
            query: User question or search query
            top_k: Number of documents to retrieve (default: 3)
            
        Returns:
            List of relevant documents with relevance scores, sorted by relevance
            
        Example:
            >>> retriever = RAGRetriever(knowledge_base)
            >>> results = retriever.retrieve("How do I deploy?", top_k=3)
            >>> for result in results:
            ...     print(f"{result['document']['title']}: {result['relevance_score']:.2f}")
        """
        # Convert query to TF-IDF vector using fitted vectorizer
        query_vector = self.vectorizer.transform([query])
        
        # Calculate cosine similarity between query and all documents
        # cosine_similarity returns a matrix of shape (1, num_documents)
        similarities = cosine_similarity(query_vector, self.doc_vectors)[0]
        
        # Get indices of top-k documents sorted by similarity
        # argsort returns indices in ascending order, so we reverse with [::-1]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Build results list with documents and scores
        results = []
        for idx in top_indices:
            similarity_score = float(similarities[idx])
            
            # Only include results above relevance threshold
            # This prevents returning irrelevant documents
            if similarity_score > 0.05:  # Relevance threshold
                results.append({
                    "document": self.documents[idx],
                    "relevance_score": similarity_score
                })
        
        return results
    
    def retrieve_by_id(self, doc_id: str) -> Dict[str, Any]:
        """
        Retrieve a document by its ID.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Document if found, None otherwise
        """
        for doc in self.documents:
            if doc["id"] == doc_id:
                return doc
        return None
    
    def search_multiple(self, queries: List[str], top_k: int = 3) -> Dict[str, List[Dict]]:
        """
        Search for multiple queries at once.
        
        Useful for batch operations or when you want results for multiple queries.
        
        Args:
            queries: List of queries
            top_k: Number of results per query
            
        Returns:
            Dictionary mapping query to results
        """
        results = {}
        for query in queries:
            results[query] = self.retrieve(query, top_k)
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge base.
        
        Returns:
            Dictionary with stats about documents and vocabulary
        """
        total_chars = sum(len(doc["content"]) for doc in self.documents)
        avg_chars = total_chars / len(self.documents)
        
        return {
            "num_documents": len(self.documents),
            "vocabulary_size": len(self.vectorizer.get_feature_names_out()),
            "total_characters": total_chars,
            "avg_chars_per_doc": avg_chars,
            "documents": [
                {
                    "id": doc["id"],
                    "title": doc["title"],
                    "char_count": len(doc["content"])
                }
                for doc in self.documents
            ]
        }


def test_retriever(knowledge_base: List[Dict[str, Any]]):
    """
    Test the retriever with sample queries.
    
    Args:
        knowledge_base: Knowledge base documents
    """
    print("\n" + "="*70)
    print("Testing RAG Retriever")
    print("="*70 + "\n")
    
    retriever = RAGRetriever(knowledge_base)
    
    # Test queries
    test_queries = [
        "How do I deploy to production?",
        "What should I check before deploying?",
        "What do I do if deployment fails?",
        "How do I monitor after deployment?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        print("-" * 70)
        
        results = retriever.retrieve(query, top_k=3)
        
        if not results:
            print("  No results found")
            continue
        
        for i, result in enumerate(results, 1):
            doc = result["document"]
            score = result["relevance_score"]
            print(f"  {i}. {doc['title']} (relevance: {score:.3f})")
            print(f"     ID: {doc['id']}")
    
    # Print stats
    print("\n" + "="*70)
    print("Knowledge Base Statistics")
    print("="*70)
    stats = retriever.get_stats()
    print(f"Documents: {stats['num_documents']}")
    print(f"Vocabulary: {stats['vocabulary_size']} unique terms")
    print(f"Total content: {stats['total_characters']:,} characters")
    print(f"Average per doc: {stats['avg_chars_per_doc']:,.0f} characters")


if __name__ == "__main__":
    # Test when run directly
    from knowledge_base import KNOWLEDGE_BASE
    test_retriever(KNOWLEDGE_BASE)
