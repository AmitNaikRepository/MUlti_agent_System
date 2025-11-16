"""
WebSocket connection manager for real-time workflow updates.
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import json


class ConnectionManager:
    """
    Manages WebSocket connections for real-time updates.
    Broadcasts workflow progress to all connected clients.
    """
    
    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: List[WebSocket] = []
        self.workflow_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, workflow_id: Optional[str] = None):
        """
        Accept new WebSocket connection.
        
        Args:
            websocket: WebSocket connection
            workflow_id: Optional workflow ID to subscribe to
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if workflow_id:
            if workflow_id not in self.workflow_connections:
                self.workflow_connections[workflow_id] = []
            self.workflow_connections[workflow_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove WebSocket connection.
        
        Args:
            websocket: WebSocket connection to remove
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # Remove from workflow-specific connections
        for workflow_id in list(self.workflow_connections.keys()):
            if websocket in self.workflow_connections[workflow_id]:
                self.workflow_connections[workflow_id].remove(websocket)
                
                # Clean up empty workflow connection lists
                if not self.workflow_connections[workflow_id]:
                    del self.workflow_connections[workflow_id]
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """
        Send message to specific client.
        
        Args:
            message: Message to send
            websocket: Target WebSocket
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast message to all connected clients.
        
        Args:
            message: Message to broadcast
        """
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def broadcast_to_workflow(self, workflow_id: str, message: Dict[str, Any]):
        """
        Broadcast message to clients subscribed to specific workflow.
        
        Args:
            workflow_id: Workflow ID
            message: Message to broadcast
        """
        if workflow_id not in self.workflow_connections:
            return
        
        disconnected = []
        
        for connection in self.workflow_connections[workflow_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to workflow client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)


# Global connection manager instance
manager = ConnectionManager()
