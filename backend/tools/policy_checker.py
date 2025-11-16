"""
Policy Checker - Business rules engine for customer support.
Validates requests against company policies.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class PolicyChecker:
    """
    Business rules engine that defines and checks company policies.
    """
    
    def __init__(self):
        """Initialize policy checker with business rules."""
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict[str, Dict[str, Any]]:
        """Define company policies."""
        return {
            "refund": {
                "name": "Refund Policy",
                "rules": [
                    "Returns accepted within 30 days of purchase",
                    "Items must be in original condition with tags",
                    "Full refund to original payment method",
                    "Shipping costs non-refundable (unless defective/wrong item)",
                    "Processing time: 5-7 business days"
                ],
                "time_limit_days": 30,
                "conditions": [
                    "original_condition",
                    "tags_attached",
                    "within_time_limit"
                ],
                "refund_percentage": 100,
                "shipping_refundable": False
            },
            "exchange": {
                "name": "Exchange Policy",
                "rules": [
                    "Exchanges within 30 days of purchase",
                    "Items must be unworn and in original condition",
                    "Free exchange shipping for defective/wrong items",
                    "Customer pays return shipping for size/color exchanges",
                    "Processing time: 3-5 business days"
                ],
                "time_limit_days": 30,
                "conditions": [
                    "unworn",
                    "original_condition"
                ],
                "free_shipping_conditions": ["defective", "wrong_item"]
            },
            "complaint": {
                "name": "Complaint Handling",
                "rules": [
                    "All complaints acknowledged within 24 hours",
                    "Investigation completed within 3 business days",
                    "Resolution offered based on issue severity",
                    "Customer satisfaction tracked and followed up"
                ],
                "response_time_hours": 24,
                "resolution_time_days": 3
            },
            "general_question": {
                "name": "Customer Support",
                "rules": [
                    "Response provided within 2 hours during business hours",
                    "All questions answered thoroughly",
                    "Additional resources provided when applicable",
                    "Follow-up offered if needed"
                ],
                "response_time_hours": 2
            }
        }
    
    def get_policies(self, category: str) -> str:
        """
        Get formatted policies for a category.
        
        Args:
            category: Policy category (refund, exchange, etc.)
            
        Returns:
            Formatted policy string
        """
        # Extract category from context if it's a dict
        if isinstance(category, dict):
            category = category.get('category', 'general_question')
        
        # Clean up category string
        if isinstance(category, str):
            # Try exact match first
            if category in self.policies:
                policy = self.policies[category]
            else:
                # Try to find partial match
                for key in self.policies:
                    if key in category.lower() or category.lower() in key:
                        policy = self.policies[key]
                        break
                else:
                    policy = self.policies.get('general_question', {})
        else:
            policy = self.policies.get('general_question', {})
        
        if not policy:
            return "No specific policy found. Use general customer support guidelines."
        
        rules_text = "\n".join(f"- {rule}" for rule in policy.get('rules', []))
        
        result = f"{policy.get('name', 'Policy')}:\n{rules_text}"
        
        # Add time limits if applicable
        if 'time_limit_days' in policy:
            result += f"\n\nTime Limit: {policy['time_limit_days']} days from purchase"
        
        return result
    
    def check_refund_eligibility(
        self,
        order_date: str,
        item_condition: str = "good",
        reason: str = "changed_mind"
    ) -> Dict[str, Any]:
        """
        Check if refund is eligible based on policy.
        
        Args:
            order_date: Order date (ISO format)
            item_condition: Condition of item (good, worn, damaged)
            reason: Reason for refund (changed_mind, defective, wrong_item)
            
        Returns:
            Eligibility result with reasoning
        """
        policy = self.policies['refund']
        time_limit = policy['time_limit_days']
        
        # Check time limit
        order_dt = datetime.fromisoformat(order_date.replace('Z', '+00:00'))
        days_since_order = (datetime.now(order_dt.tzinfo) - order_dt).days
        within_time_limit = days_since_order <= time_limit
        
        # Check conditions
        eligible = True
        issues = []
        
        if not within_time_limit:
            eligible = False
            issues.append(f"Order is {days_since_order} days old (limit: {time_limit} days)")
        
        if item_condition.lower() in ['worn', 'damaged', 'used']:
            if reason not in ['defective', 'wrong_item']:
                eligible = False
                issues.append("Item is not in original condition")
        
        # Determine refund amount
        refund_percentage = policy['refund_percentage'] if eligible else 0
        
        # Check shipping refund
        shipping_refundable = reason in ['defective', 'wrong_item']
        
        return {
            "eligible": eligible,
            "refund_percentage": refund_percentage,
            "shipping_refundable": shipping_refundable,
            "issues": issues,
            "days_since_order": days_since_order,
            "time_limit": time_limit,
            "reasoning": self._format_eligibility_reasoning(
                eligible, within_time_limit, item_condition, reason, issues
            )
        }
    
    def _format_eligibility_reasoning(
        self,
        eligible: bool,
        within_time_limit: bool,
        item_condition: str,
        reason: str,
        issues: List[str]
    ) -> str:
        """Format eligibility reasoning."""
        if eligible:
            return f"Refund approved. Item is within return window and meets policy requirements. Reason: {reason}"
        else:
            return f"Refund denied. Issues: {'; '.join(issues)}"
    
    def calculate_refund_amount(
        self,
        order_total: float,
        shipping_cost: float = 0.0,
        refund_percentage: int = 100,
        include_shipping: bool = False
    ) -> Dict[str, float]:
        """
        Calculate refund amount.
        
        Args:
            order_total: Total order amount
            shipping_cost: Shipping cost
            refund_percentage: Percentage to refund (0-100)
            include_shipping: Whether to include shipping in refund
            
        Returns:
            Refund breakdown
        """
        product_refund = (order_total - shipping_cost) * (refund_percentage / 100)
        shipping_refund = shipping_cost if include_shipping else 0.0
        total_refund = product_refund + shipping_refund
        
        return {
            "product_refund": round(product_refund, 2),
            "shipping_refund": round(shipping_refund, 2),
            "total_refund": round(total_refund, 2)
        }
