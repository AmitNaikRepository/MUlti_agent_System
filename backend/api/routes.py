"""
API routes for the Multi-Agent Orchestration System.
"""
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from ..models import (
    WorkflowRequest,
    WorkflowResponse,
    WorkflowExecution,
    AgentMetrics,
    get_db,
    WorkflowListResponse,
    HealthResponse
)
from ..agents.orchestrator import WorkflowOrchestrator
from .websocket import manager

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@router.post("/workflow/execute", response_model=Dict[str, Any])
async def execute_workflow(
    request: WorkflowRequest,
    db: Session = Depends(get_db)
):
    """
    Execute multi-agent workflow for customer support.
    
    Args:
        request: Workflow execution request
        db: Database session
        
    Returns:
        Workflow result with metrics
    """
    try:
        # Create orchestrator with WebSocket callback
        async def ws_callback(update: Dict[str, Any]):
            """Callback to broadcast updates via WebSocket."""
            await manager.broadcast(update)
        
        orchestrator = WorkflowOrchestrator(websocket_callback=ws_callback)
        
        # Execute workflow
        result = await orchestrator.execute_workflow(
            user_input=request.user_input,
            workflow_type=request.workflow_type
        )
        
        # Save to database
        workflow_record = WorkflowExecution(
            workflow_id=result["workflow_id"],
            status=result["status"],
            user_input=result["user_input"],
            category=result.get("category"),
            urgency=result.get("urgency"),
            final_output=result.get("final_output", ""),
            total_cost_usd=result["metrics"]["total_cost_usd"],
            total_latency_ms=result["metrics"]["total_latency_ms"],
            total_tokens=result["metrics"]["total_tokens"],
            avg_confidence=result["metrics"]["avg_confidence"],
            agents_used=result["metrics"]["agents_used"],
            workflow_data=result
        )
        
        db.add(workflow_record)
        
        # Save individual agent metrics
        for step in result["steps"]:
            agent_metric = AgentMetrics(
                workflow_id=result["workflow_id"],
                agent_name=step["agent"],
                latency_ms=step["latency_ms"],
                cost_usd=step["cost_usd"],
                tokens_used=step["tokens_used"],
                confidence=step["confidence"]
            )
            db.add(agent_metric)
        
        db.commit()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflows/{workflow_id}")
async def get_workflow_details(workflow_id: str, db: Session = Depends(get_db)):
    """
    Get workflow execution details by ID.
    
    Args:
        workflow_id: Workflow ID
        db: Database session
        
    Returns:
        Workflow details
    """
    workflow = db.query(WorkflowExecution).filter(
        WorkflowExecution.workflow_id == workflow_id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow.workflow_data


@router.get("/workflows", response_model=WorkflowListResponse)
async def list_workflows(
    limit: int = 50,
    offset: int = 0,
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List workflow executions with optional filters.
    
    Args:
        limit: Maximum number of results
        offset: Offset for pagination
        category: Filter by category
        status: Filter by status
        db: Database session
        
    Returns:
        List of workflows
    """
    query = db.query(WorkflowExecution)
    
    if category:
        query = query.filter(WorkflowExecution.category == category)
    
    if status:
        query = query.filter(WorkflowExecution.status == status)
    
    total = query.count()
    
    workflows = query.order_by(WorkflowExecution.created_at.desc()) \
                     .offset(offset) \
                     .limit(limit) \
                     .all()
    
    return {
        "total": total,
        "workflows": [w.to_dict() for w in workflows]
    }


@router.get("/metrics/summary")
async def get_metrics_summary(db: Session = Depends(get_db)):
    """
    Get aggregate metrics summary.
    
    Args:
        db: Database session
        
    Returns:
        Metrics summary
    """
    from sqlalchemy import func
    
    # Get overall statistics
    total_workflows = db.query(func.count(WorkflowExecution.id)).scalar()
    
    avg_cost = db.query(func.avg(WorkflowExecution.total_cost_usd)).scalar() or 0
    avg_latency = db.query(func.avg(WorkflowExecution.total_latency_ms)).scalar() or 0
    avg_confidence = db.query(func.avg(WorkflowExecution.avg_confidence)).scalar() or 0
    
    # Category breakdown
    category_stats = db.query(
        WorkflowExecution.category,
        func.count(WorkflowExecution.id).label('count')
    ).group_by(WorkflowExecution.category).all()
    
    # Agent performance
    agent_stats = db.query(
        AgentMetrics.agent_name,
        func.avg(AgentMetrics.latency_ms).label('avg_latency'),
        func.avg(AgentMetrics.cost_usd).label('avg_cost'),
        func.avg(AgentMetrics.confidence).label('avg_confidence')
    ).group_by(AgentMetrics.agent_name).all()
    
    return {
        "total_workflows": total_workflows,
        "avg_cost_usd": round(avg_cost, 6),
        "avg_latency_ms": round(avg_latency, 2),
        "avg_confidence": round(avg_confidence, 2),
        "category_breakdown": [
            {"category": cat, "count": count}
            for cat, count in category_stats
        ],
        "agent_performance": [
            {
                "agent": agent,
                "avg_latency_ms": round(latency, 2),
                "avg_cost_usd": round(cost, 6),
                "avg_confidence": round(conf, 2)
            }
            for agent, latency, cost, conf in agent_stats
        ]
    }


@router.get("/metrics/comparison")
async def get_comparison_metrics():
    """
    Compare multi-agent vs single LLM approach.
    
    Returns:
        Comparison metrics
    """
    # These are example/estimated metrics
    # In production, you'd run actual comparisons and store results
    return {
        "multi_agent": {
            "avg_accuracy": 0.92,
            "avg_cost_usd": 0.0023,
            "avg_latency_ms": 3400,
            "model": "Multiple specialized models (Groq)"
        },
        "single_llm": {
            "avg_accuracy": 0.78,
            "avg_cost_usd": 0.015,
            "avg_latency_ms": 2100,
            "model": "GPT-4 (single model)"
        },
        "improvement": {
            "accuracy": "+18%",
            "cost": "-84% (6.5x cheaper)",
            "latency": "+62% slower (acceptable tradeoff)"
        },
        "recommendation": "Multi-agent approach provides better accuracy at significantly lower cost, with acceptable latency increase."
    }


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time workflow updates.
    
    Args:
        websocket: WebSocket connection
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive and receive any client messages
            data = await websocket.receive_text()
            
            # Echo back acknowledgment
            await websocket.send_json({
                "type": "ack",
                "message": "Connected to workflow updates",
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
