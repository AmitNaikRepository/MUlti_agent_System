"""
Classifier Agent - Categorizes customer support requests.
Determines the type of request and urgency level.
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig


class ClassifierAgent(BaseAgent):
    """
    Classifies customer support requests into categories:
    - refund: Customer wants money back
    - exchange: Customer wants to swap product
    - complaint: Customer is unhappy but no specific action
    - general_question: Customer needs information
    
    Also determines urgency level: low, medium, high
    """
    
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        """Initialize classifier agent with optimized configuration."""
        config = AgentConfig(
            name="Classifier",
            model=model,
            temperature=0.3,  # Lower temperature for consistent classification
            max_tokens=500,
            system_prompt="""You are a customer support classification expert. 
Your job is to analyze customer messages and accurately categorize them.

Categories:
- refund: Customer wants their money back
- exchange: Customer wants to swap/replace a product
- complaint: Customer is expressing dissatisfaction
- general_question: Customer needs information or help

Urgency Levels:
- high: Angry customer, legal threats, time-sensitive (same-day delivery issue)
- medium: Product defect, wrong item received, payment issues
- low: General questions, tracking info, policy questions

Always respond in valid JSON format with category, urgency, and reasoning.
Be concise but accurate in your reasoning."""
        )
        super().__init__(config)
    
    def _build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Build classification prompt.
        
        Args:
            input_data: Must contain 'message' key with customer message
            context: Not used for classifier (first agent in workflow)
            
        Returns:
            Formatted prompt for classification
        """
        customer_message = input_data.get('message', '')
        
        prompt = f"""Analyze this customer support message and classify it.

Customer Message:
"{customer_message}"

Respond with valid JSON only:
{{
    "category": "refund|exchange|complaint|general_question",
    "urgency": "low|medium|high",
    "reasoning": "Brief explanation of your classification",
    "confidence": 0.0-1.0
}}"""
        
        return prompt
    
    def get_category(self, result_output: str) -> str:
        """
        Extract category from agent result.
        
        Args:
            result_output: Agent output string
            
        Returns:
            Category name or 'unknown'
        """
        data = self._extract_json(result_output)
        if data:
            return data.get('category', 'unknown')
        return 'unknown'
    
    def get_urgency(self, result_output: str) -> str:
        """
        Extract urgency from agent result.
        
        Args:
            result_output: Agent output string
            
        Returns:
            Urgency level or 'medium'
        """
        data = self._extract_json(result_output)
        if data:
            return data.get('urgency', 'medium')
        return 'medium'
