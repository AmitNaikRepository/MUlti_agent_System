"""
Research Agent - Searches knowledge base for relevant information.
Retrieves product info, policies, and order details.
"""
from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentConfig


class ResearchAgent(BaseAgent):
    """
    Researches relevant information from knowledge base.
    Searches for:
    - Product information and specifications
    - Company policies (refund, exchange, shipping)
    - Order details and history
    - FAQ and common solutions
    """
    
    def __init__(self, knowledge_base, model: str = "llama-3.1-8b-instant"):
        """
        Initialize research agent.
        
        Args:
            knowledge_base: Knowledge base tool for searching information
            model: Groq model to use
        """
        self.knowledge_base = knowledge_base
        
        config = AgentConfig(
            name="Researcher",
            model=model,
            temperature=0.4,
            max_tokens=800,
            system_prompt="""You are a research specialist for customer support.
Your job is to extract and summarize relevant information from provided documents.

Given a customer query and relevant documents:
1. Identify key information that answers the query
2. Extract specific details (prices, policies, dates, etc.)
3. Summarize clearly and concisely
4. Note any missing information

Always provide factual information based on the documents provided.
Do not make up information that isn't in the documents."""
        )
        super().__init__(config)
    
    def _build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Build research prompt with knowledge base results.
        
        Args:
            input_data: Must contain 'query' or 'message'
            context: Contains 'category' from classifier
            
        Returns:
            Formatted prompt with relevant documents
        """
        query = input_data.get('query') or input_data.get('message', '')
        category = context.get('category', 'general')
        
        # Search knowledge base for relevant information
        search_results = self.knowledge_base.search(query, category=category)
        
        prompt = f"""Research the following customer query and extract relevant information.

Customer Query:
"{query}"

Query Category: {category}

Relevant Documents:
{search_results}

Please provide:
1. Key information that addresses the query
2. Relevant policies or product details
3. Any order-specific information if applicable
4. Missing information that would be needed

Respond in JSON:
{{
    "key_findings": "Main information found",
    "relevant_policies": "Applicable policies",
    "order_info": "Order details if found",
    "missing_info": "What additional info is needed",
    "confidence": 0.0-1.0
}}"""
        
        return prompt
