"""
Writer Agent - Generates professional customer-facing responses.
Crafts empathetic, clear, and helpful email responses.
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig


class WriterAgent(BaseAgent):
    """
    Generates professional customer support responses.
    
    Creates emails that are:
    - Empathetic and understanding
    - Clear and concise
    - Professional in tone
    - Action-oriented with next steps
    """
    
    def __init__(self, model: str = "mixtral-8x7b-32768"):
        """
        Initialize writer agent.
        Uses more capable model for better writing quality.
        
        Args:
            model: Groq model to use (default: mixtral for better writing)
        """
        config = AgentConfig(
            name="Writer",
            model=model,
            temperature=0.7,  # Higher temperature for more natural writing
            max_tokens=1200,
            system_prompt="""You are an expert customer support email writer.
Your emails are known for being empathetic, clear, and professional.

Email Writing Guidelines:
1. Start with empathy - acknowledge the customer's situation
2. Be clear and direct - explain the resolution or next steps
3. Use professional but warm tone
4. Include specific details (amounts, dates, actions)
5. End with clear next steps and contact info
6. Keep it concise - 3-4 short paragraphs max

Tone Examples:
✓ "I understand how frustrating it must be..."
✓ "I'd be happy to help you with this..."
✓ "Here's what we can do..."
✗ Avoid: "Unfortunately...", "I'm sorry but we can't..."

Write complete, ready-to-send emails."""
        )
        super().__init__(config)
    
    def _build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Build writing prompt with all context from previous agents.
        
        Args:
            input_data: Optional additional instructions
            context: Contains validation, research, category from previous agents
            
        Returns:
            Formatted writing prompt
        """
        validation = context.get('validation', {})
        research = context.get('research', {})
        category = context.get('category', 'general')
        
        # Extract validation details
        approved = "Unknown"
        amount = "N/A"
        required_actions = []
        validation_reasoning = ""
        
        if isinstance(validation, dict):
            approved = "Approved" if validation.get('approved') else "Denied"
            amount = validation.get('amount', 'N/A')
            required_actions = validation.get('required_actions', [])
            validation_reasoning = validation.get('reasoning', '')
        elif isinstance(validation, str):
            validation_reasoning = validation
        
        actions_text = "\n".join(f"- {action}" for action in required_actions) if required_actions else "None"
        
        prompt = f"""Write a professional customer support email based on this situation.

Request Type: {category}
Decision: {approved}
Amount: {amount}
Validation Reasoning: {validation_reasoning}

Research Findings:
{research}

Required Customer Actions:
{actions_text}

Write a complete email response that:
1. Acknowledges the customer's situation with empathy
2. Clearly explains the resolution ({approved})
3. Provides specific details (amount: {amount})
4. Lists any required actions
5. Ends with next steps and contact information

The email should be ready to send - no placeholders like [Customer Name].
Use "Dear Customer" or "Hello" as greeting.

Write the email now (no JSON, just the email text):"""
        
        return prompt
