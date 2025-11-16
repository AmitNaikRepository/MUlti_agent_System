"""
QA Agent - Reviews generated responses for quality.
Evaluates accuracy, tone, completeness, and clarity.
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig


class QAAgent(BaseAgent):
    """
    Quality Assurance agent that reviews customer support responses.
    
    Evaluates:
    - Accuracy: Does it match validation results?
    - Tone: Professional and empathetic?
    - Completeness: All questions answered?
    - Clarity: Easy to understand?
    """
    
    def __init__(self, model: str = "llama-3.1-70b-versatile"):
        """
        Initialize QA agent.
        Uses more capable model for thorough review.
        
        Args:
            model: Groq model to use (default: llama-70b for better analysis)
        """
        config = AgentConfig(
            name="QA",
            model=model,
            temperature=0.3,  # Lower temperature for consistent evaluation
            max_tokens=1000,
            system_prompt="""You are a quality assurance expert for customer support.
Your job is to review email responses and ensure they meet high quality standards.

Evaluation Criteria:
1. ACCURACY (1-10): Does the email match the validation decision and amounts?
2. TONE (1-10): Is it empathetic, professional, and customer-friendly?
3. COMPLETENESS (1-10): Are all points addressed? Clear next steps?
4. CLARITY (1-10): Is it easy to understand? Free of jargon?

For each criterion:
- 9-10: Excellent, ready to send
- 7-8: Good, minor improvements possible
- 5-6: Acceptable, some issues
- 1-4: Poor, needs revision

Provide specific, actionable feedback for improvements.
Be thorough but fair in your evaluation."""
        )
        super().__init__(config)
    
    def _build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Build QA review prompt.
        
        Args:
            input_data: Must contain 'draft_email'
            context: Contains validation, research for comparison
            
        Returns:
            Formatted QA prompt
        """
        draft_email = input_data.get('draft_email', '')
        validation = context.get('validation', {})
        category = context.get('category', 'general')
        
        # Extract expected details from validation
        approved = "Unknown"
        amount = "N/A"
        if isinstance(validation, dict):
            approved = "Approved" if validation.get('approved') else "Denied"
            amount = validation.get('amount', 'N/A')
        
        prompt = f"""Review this customer support email for quality.

REQUEST TYPE: {category}
EXPECTED DECISION: {approved}
EXPECTED AMOUNT: {amount}

VALIDATION DETAILS:
{validation}

EMAIL TO REVIEW:
---
{draft_email}
---

Evaluate the email on these criteria (score 1-10 each):

1. ACCURACY: Does the email correctly state the decision ({approved}) and amount ({amount})?
2. TONE: Is it empathetic, professional, and friendly?
3. COMPLETENESS: Are all necessary details included? Clear next steps?
4. CLARITY: Is it easy to understand? Well-structured?

Respond in JSON:
{{
    "accuracy_score": 1-10,
    "tone_score": 1-10,
    "completeness_score": 1-10,
    "clarity_score": 1-10,
    "overall_score": 1-10,
    "strengths": ["strength1", "strength2"],
    "improvements": ["improvement1", "improvement2"],
    "recommendation": "APPROVE|REVISE|REJECT",
    "reasoning": "Overall assessment",
    "confidence": 0.0-1.0
}}"""
        
        return prompt
    
    def is_approved(self, result_output: str) -> bool:
        """
        Check if QA approved the email.
        
        Args:
            result_output: QA agent output
            
        Returns:
            True if email is approved for sending
        """
        data = self._extract_json(result_output)
        if data:
            recommendation = data.get('recommendation', 'REVISE')
            overall_score = data.get('overall_score', 0)
            return recommendation == 'APPROVE' or overall_score >= 7
        return False
    
    def get_overall_score(self, result_output: str) -> float:
        """
        Extract overall quality score.
        
        Args:
            result_output: QA agent output
            
        Returns:
            Overall score (0-10)
        """
        data = self._extract_json(result_output)
        if data:
            return float(data.get('overall_score', 0))
        return 0.0
