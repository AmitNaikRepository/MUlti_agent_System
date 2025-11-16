"""
Validator Agent - Validates requests against business rules.
Determines eligibility for refunds, exchanges, etc.
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig


class ValidatorAgent(BaseAgent):
    """
    Validates customer requests against business rules and policies.
    
    Checks:
    - Refund eligibility (time limits, condition requirements)
    - Exchange eligibility
    - Policy compliance
    - Calculates refund/exchange amounts
    """
    
    def __init__(self, policy_checker, model: str = "llama-3.1-8b-instant"):
        """
        Initialize validator agent.
        
        Args:
            policy_checker: Policy checking tool
            model: Groq model to use
        """
        self.policy_checker = policy_checker
        
        config = AgentConfig(
            name="Validator",
            model=model,
            temperature=0.2,  # Very low temperature for consistent rule application
            max_tokens=700,
            system_prompt="""You are a policy validation expert for customer support.
Your job is to determine if customer requests comply with company policies.

You must:
1. Apply business rules strictly and consistently
2. Calculate exact refund/exchange amounts
3. Identify required actions (return shipping, photos, etc.)
4. Clearly state approval or denial with reasoning

Be fair but follow policies exactly. If something is unclear, note it."""
        )
        super().__init__(config)
    
    def _build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Build validation prompt with policies and research findings.
        
        Args:
            input_data: Contains 'request' or 'message'
            context: Contains 'category', 'research' from previous agents
            
        Returns:
            Formatted validation prompt
        """
        request = input_data.get('request') or input_data.get('message', '')
        category = context.get('category', 'general')
        research_findings = context.get('research', {})
        
        # Get applicable policies
        policies = self.policy_checker.get_policies(category)
        
        # Extract order info from research if available
        order_info = "No order information available"
        if isinstance(research_findings, dict):
            order_info = research_findings.get('order_info', order_info)
        
        prompt = f"""Validate this customer request against company policies.

Request Type: {category}
Customer Request: "{request}"

Order Information:
{order_info}

Applicable Policies:
{policies}

Research Findings:
{research_findings}

Determine:
1. Is the request eligible/approved? (yes/no)
2. What is the refund/exchange amount? (if applicable)
3. What actions are required? (return item, provide photos, etc.)
4. What is the reasoning for approval/denial?

Respond in JSON:
{{
    "approved": true/false,
    "amount": "dollar amount or N/A",
    "required_actions": ["action1", "action2"],
    "reasoning": "Clear explanation",
    "policy_references": "Which policies apply",
    "confidence": 0.0-1.0
}}"""
        
        return prompt
