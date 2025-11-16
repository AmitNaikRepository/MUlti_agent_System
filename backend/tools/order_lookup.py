"""
Order Lookup - Simulated order database for customer support.
Retrieves order details, status, and history.
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import re


class OrderLookup:
    """
    Simulated order database.
    In production, this would query a real database or API.
    """
    
    def __init__(self):
        """Initialize with sample orders."""
        self.orders = self._get_sample_orders()
    
    def _get_sample_orders(self) -> Dict[str, Dict[str, Any]]:
        """Generate sample order data."""
        return {
            "12345": {
                "order_id": "12345",
                "customer_email": "customer@example.com",
                "order_date": (datetime.now() - timedelta(days=10)).isoformat(),
                "status": "delivered",
                "items": [
                    {
                        "product": "iPhone 15",
                        "quantity": 1,
                        "price": 799.00,
                        "sku": "IPHONE15-BLK-128"
                    }
                ],
                "total": 799.00,
                "shipping_address": "123 Main St, Anytown, USA",
                "tracking_number": "1Z999AA10123456784",
                "delivery_date": (datetime.now() - timedelta(days=3)).isoformat()
            },
            "67890": {
                "order_id": "67890",
                "customer_email": "john@example.com",
                "order_date": (datetime.now() - timedelta(days=5)).isoformat(),
                "status": "in_transit",
                "items": [
                    {
                        "product": "iPhone 15 Pro",
                        "quantity": 1,
                        "price": 999.00,
                        "sku": "IPHONE15PRO-TIT-256"
                    }
                ],
                "total": 999.00,
                "shipping_address": "456 Oak Ave, Other City, USA",
                "tracking_number": "1Z999AA10123456785",
                "estimated_delivery": (datetime.now() + timedelta(days=2)).isoformat()
            },
            "11111": {
                "order_id": "11111",
                "customer_email": "sarah@example.com",
                "order_date": (datetime.now() - timedelta(days=45)).isoformat(),
                "status": "delivered",
                "items": [
                    {
                        "product": "iPhone 15",
                        "quantity": 1,
                        "price": 799.00,
                        "sku": "IPHONE15-PINK-256"
                    }
                ],
                "total": 799.00,
                "shipping_address": "789 Elm St, Some Town, USA",
                "tracking_number": "1Z999AA10123456786",
                "delivery_date": (datetime.now() - timedelta(days=40)).isoformat()
            }
        }
    
    def lookup_order(self, query: str) -> Optional[str]:
        """
        Look up order by order number.
        Extracts order number from query and returns formatted order details.
        
        Args:
            query: Customer query containing order number
            
        Returns:
            Formatted order details or None if not found
        """
        # Extract order number from query (looks for patterns like #12345 or Order 12345)
        order_num = self._extract_order_number(query)
        
        if not order_num:
            return None
        
        order = self.orders.get(order_num)
        if not order:
            return f"Order #{order_num} not found in system."
        
        return self._format_order(order)
    
    def _extract_order_number(self, query: str) -> Optional[str]:
        """
        Extract order number from query text.
        
        Args:
            query: Text containing order number
            
        Returns:
            Order number or None
        """
        # Look for patterns: #12345, Order 12345, order #12345, etc.
        patterns = [
            r'#(\d+)',
            r'order\s+#?(\d+)',
            r'order\s+number\s+#?(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _format_order(self, order: Dict[str, Any]) -> str:
        """
        Format order details for display.
        
        Args:
            order: Order dictionary
            
        Returns:
            Formatted order string
        """
        items_text = "\n".join([
            f"  - {item['product']} (Qty: {item['quantity']}) - ${item['price']:.2f}"
            for item in order['items']
        ])
        
        result = f"""Order #{order['order_id']}
Status: {order['status'].upper()}
Order Date: {order['order_date'][:10]}
Total: ${order['total']:.2f}

Items:
{items_text}

Shipping: {order['shipping_address']}
Tracking: {order['tracking_number']}"""
        
        if 'delivery_date' in order:
            result += f"\nDelivered: {order['delivery_date'][:10]}"
        elif 'estimated_delivery' in order:
            result += f"\nEstimated Delivery: {order['estimated_delivery'][:10]}"
        
        return result
    
    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Get raw order data.
        
        Args:
            order_id: Order ID
            
        Returns:
            Order dict or None
        """
        return self.orders.get(order_id)
    
    def is_within_refund_window(self, order_id: str, days: int = 30) -> bool:
        """
        Check if order is within refund window.
        
        Args:
            order_id: Order ID
            days: Refund window in days (default 30)
            
        Returns:
            True if within window, False otherwise
        """
        order = self.get_order(order_id)
        if not order:
            return False
        
        order_date = datetime.fromisoformat(order['order_date'])
        days_ago = (datetime.now() - order_date).days
        
        return days_ago <= days
