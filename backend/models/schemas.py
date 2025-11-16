"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class WorkflowRequest(BaseModel):
    """Request to execute a workflow."""
    user_input: str = Field(..., min_length=1, description="Customer message or query")
    workflow_type: str = Field(default="customer_support", description="Type of workflow")


class AgentStepResult(BaseModel):
    """Result from a single agent step."""
    agent: str
    output: str
    reasoning: str
    confidence: float
    cost_usd: float
    latency_ms: int
    tokens_used: int


class WorkflowMetrics(BaseModel):
    """Aggregate workflow metrics."""
    total_cost_usd: float
    total_latency_ms: int
    total_tokens: int
    avg_confidence: float
    agents_used: int
    workflow_duration_ms: int


class WorkflowResponse(BaseModel):
    """Response from workflow execution."""
    workflow_id: str
    status: str
    user_input: str
    category: Optional[str] = None
    urgency: Optional[str] = None
    final_output: str
    qa_review: Optional[Dict[str, Any]] = None
    steps: List[AgentStepResult]
    metrics: WorkflowMetrics
    timestamp: str


class ComparisonRequest(BaseModel):
    """Request to compare multi-agent vs single LLM."""
    user_input: str
    include_single_llm: bool = Field(default=True, description="Include single LLM comparison")


class MetricsFilter(BaseModel):
    """Filter for metrics queries."""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    limit: int = Field(default=100, le=1000)


class WorkflowListResponse(BaseModel):
    """List of workflow executions."""
    total: int
    workflows: List[Dict[str, Any]]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str = "1.0.0"
