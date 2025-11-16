"""
Knowledge Base - Simulated document search for customer support.
Provides product info, policies, and FAQs.
"""
import json
from typing import List, Dict, Any, Optional
from pathlib import Path


class KnowledgeBase:
    """
    Simulated knowledge base for customer support.
    In production, this would connect to a vector database or search engine.
    """
    
    def __init__(self, data_path: str = "./data/knowledge_base.json"):
        """
        Initialize knowledge base.
        
        Args:
            data_path: Path to knowledge base JSON file
        """
        self.data_path = Path(data_path)
        self.documents = self._load_documents()
    
    def _load_documents(self) -> List[Dict[str, Any]]:
        """Load documents from JSON file."""
        if self.data_path.exists():
            with open(self.data_path, 'r') as f:
                return json.load(f)
        else:
            # Return default documents if file doesn't exist
            return self._get_default_documents()
    
    def _get_default_documents(self) -> List[Dict[str, Any]]:
        """Default knowledge base documents."""
        return [
            {
                "id": "refund-policy",
                "category": "policy",
                "title": "Refund Policy",
                "content": """Our refund policy allows returns within 30 days of purchase. 
Items must be in original condition with tags attached. 
Full refund will be issued to original payment method within 5-7 business days.
Shipping costs are non-refundable unless item was defective or wrong item shipped."""
            },
            {
                "id": "exchange-policy",
                "category": "policy",
                "title": "Exchange Policy",
                "content": """Exchanges accepted within 30 days of purchase.
Items must be unworn and in original condition.
Free exchange shipping for defective items or wrong items shipped.
Customer pays return shipping for size/color exchanges."""
            },
            {
                "id": "shipping-policy",
                "category": "policy",
                "title": "Shipping Policy",
                "content": """Standard shipping: 5-7 business days ($5.99)
Express shipping: 2-3 business days ($12.99)
Free shipping on orders over $50
Tracking provided via email once shipped"""
            },
            {
                "id": "product-iphone-15",
                "category": "product",
                "title": "iPhone 15 Pro",
                "content": """iPhone 15 Pro - Premium smartphone
Price: $999
Features: A17 Pro chip, ProMotion display, 48MP camera
Colors: Natural Titanium, Blue Titanium, White Titanium, Black Titanium
Storage: 128GB, 256GB, 512GB, 1TB"""
            },
            {
                "id": "product-iphone-15-regular",
                "category": "product",
                "title": "iPhone 15",
                "content": """iPhone 15 - Standard model
Price: $799
Features: A16 Bionic chip, Super Retina display, 48MP camera
Colors: Pink, Yellow, Green, Blue, Black
Storage: 128GB, 256GB, 512GB"""
            }
        ]
    
    def search(self, query: str, category: Optional[str] = None, top_k: int = 3) -> str:
        """
        Search knowledge base for relevant documents.
        
        Args:
            query: Search query
            category: Filter by category (refund, exchange, product, etc.)
            top_k: Number of results to return
            
        Returns:
            Formatted search results as string
        """
        # Simple keyword-based search (in production, use vector similarity)
        query_lower = query.lower()
        results = []
        
        for doc in self.documents:
            # Calculate relevance score (simple keyword matching)
            score = 0
            content_lower = (doc['title'] + ' ' + doc['content']).lower()
            
            # Check category match
            if category:
                if category.lower() in doc.get('category', '').lower():
                    score += 5
            
            # Check keyword matches
            keywords = query_lower.split()
            for keyword in keywords:
                if len(keyword) > 2 and keyword in content_lower:
                    score += content_lower.count(keyword)
            
            if score > 0:
                results.append({
                    'doc': doc,
                    'score': score
                })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # Format results
        if not results:
            return "No relevant documents found in knowledge base."
        
        formatted_results = []
        for i, result in enumerate(results[:top_k], 1):
            doc = result['doc']
            formatted_results.append(
                f"[Document {i}] {doc['title']}\n{doc['content']}"
            )
        
        return "\n\n".join(formatted_results)
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific document by ID.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Document dict or None
        """
        for doc in self.documents:
            if doc.get('id') == doc_id:
                return doc
        return None
