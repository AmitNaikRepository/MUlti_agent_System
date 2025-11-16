"""
Workflow Orchestrator - Coordinates multi-agent workflow execution.
Manages agent execution order, state, and real-time updates.
"""
import uuid
import time
import json
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime

from .classifier_agent import ClassifierAgent
from .research_agent import ResearchAgent
from .validator_agent import ValidatorAgent
from .writer_agent import WriterAgent
from .qa_agent import QAAgent
from ..tools import KnowledgeBase, OrderLookup, PolicyChecker


class WorkflowOrchestrator:
    """
    Orchestrates the multi-agent workflow for customer support.
    
    Workflow Steps:
    1. Classify: Categorize the request
    2. Research: Find relevant information
    3. Validate: Check against policies
    4. Write: Generate response
    5. QA: Review quality
    
    Emits real-time updates via callback for UI updates.
    """
    
    def __init__(self, websocket_callback: Optional[Callable] = None):
        """
        Initialize orchestrator with agents and tools.
        
        Args:
            websocket_callback: Optional callback for real-time updates
        """
        # Initialize tools
        self.knowledge_base = KnowledgeBase()
        self.order_lookup = OrderLookup()
        self.policy_checker = PolicyChecker()
        
        # Initialize agents
        self.agents = {
            "classifier": ClassifierAgent(model="llama-3.1-8b-instant"),
            "researcher": ResearchAgent(
                knowledge_base=self.knowledge_base,
                model="llama-3.1-8b-instant"
            ),
            "validator": ValidatorAgent(
                policy_checker=self.policy_checker,
                model="llama-3.1-8b-instant"
            ),
            "writer": WriterAgent(model="mixtral-8x7b-32768"),
            "qa": QAAgent(model="llama-3.1-70b-versatile")
        }
        
        # Workflow state
        self.state: Dict[str, Any] = {}
        self.websocket_callback = websocket_callback
    
    async def execute_workflow(
        self,
        user_input: str,
        workflow_type: str = "customer_support"
    ) -> Dict[str, Any]:
        """
        Execute the complete multi-agent workflow.
        
        Args:
            user_input: Customer message/query
            workflow_type: Type of workflow (default: customer_support)
            
        Returns:
            Complete workflow result with metrics
        """
        workflow_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Initialize state
        self.state = {
            "workflow_id": workflow_id,
            "user_input": user_input,
            "workflow_type": workflow_type,
            "timestamp": datetime.now().isoformat()
        }
        
        results: List[Dict[str, Any]] = []
        
        try:
            # Step 1: Classify the request
            classify_result = await self._execute_agent_step(
                agent_name="classifier",
                input_data={"message": user_input},
                step_number=1,
                total_steps=5
            )
            results.append(classify_result)
            
            # Extract category for next steps
            category_data = self.agents["classifier"]._extract_json(classify_result.output)
            if category_data:
                self.state["category"] = category_data.get("category", "general_question")
                self.state["urgency"] = category_data.get("urgency", "medium")
            else:
                self.state["category"] = "general_question"
                self.state["urgency"] = "medium"
            
            # Step 2: Research relevant information
            research_input = {
                "query": user_input,
                "message": user_input
            }
            
            # Try to find order information
            order_info = self.order_lookup.lookup_order(user_input)
            if order_info:
                self.state["order_info"] = order_info
            
            research_result = await self._execute_agent_step(
                agent_name="researcher",
                input_data=research_input,
                step_number=2,
                total_steps=5
            )
            results.append(research_result)
            
            # Extract research findings
            research_data = self.agents["researcher"]._extract_json(research_result.output)
            self.state["research"] = research_data or research_result.output
            
            # Step 3: Validate the request
            validate_result = await self._execute_agent_step(
                agent_name="validator",
                input_data={"request": user_input, "message": user_input},
                step_number=3,
                total_steps=5
            )
            results.append(validate_result)
            
            # Extract validation decision
            validation_data = self.agents["validator"]._extract_json(validate_result.output)
            self.state["validation"] = validation_data or validate_result.output
            
            # Step 4: Write customer response
            write_result = await self._execute_agent_step(
                agent_name="writer",
                input_data={},
                step_number=4,
                total_steps=5
            )
            results.append(write_result)
            
            self.state["draft"] = write_result.output
            
            # Step 5: QA review
            qa_result = await self._execute_agent_step(
                agent_name="qa",
                input_data={"draft_email": write_result.output},
                step_number=5,
                total_steps=5
            )
            results.append(qa_result)
            
            # Extract QA scores
            qa_data = self.agents["qa"]._extract_json(qa_result.output)
            self.state["qa_review"] = qa_data or qa_result.output
            
            # Calculate aggregate metrics
            total_cost = sum(r.cost_usd for r in results)
            total_latency = sum(r.latency_ms for r in results)
            total_tokens = sum(r.tokens_used for r in results)
            
            # Calculate average confidence
            avg_confidence = sum(r.confidence for r in results) / len(results)
            
            workflow_result = {
                "workflow_id": workflow_id,
                "status": "completed",
                "user_input": user_input,
                "category": self.state.get("category"),
                "urgency": self.state.get("urgency"),
                "final_output": write_result.output,
                "qa_review": qa_data,
                "steps": [
                    {
                        "agent": r.agent_name,
                        "output": r.output,
                        "reasoning": r.reasoning,
                        "confidence": r.confidence,
                        "cost_usd": r.cost_usd,
                        "latency_ms": r.latency_ms,
                        "tokens_used": r.tokens_used
                    }
                    for r in results
                ],
                "metrics": {
                    "total_cost_usd": round(total_cost, 6),
                    "total_latency_ms": total_latency,
                    "total_tokens": total_tokens,
                    "avg_confidence": round(avg_confidence, 2),
                    "agents_used": len(results),
                    "workflow_duration_ms": int((time.time() - start_time) * 1000)
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # Send completion update
            await self._emit_status(workflow_id, "workflow", "completed", workflow_result)
            
            return workflow_result
            
        except Exception as e:
            # Handle workflow errors
            error_result = {
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e),
                "error_type": type(e).__name__,
                "steps": [
                    {
                        "agent": r.agent_name,
                        "output": r.output,
                        "cost_usd": r.cost_usd,
                        "latency_ms": r.latency_ms
                    }
                    for r in results
                ],
                "timestamp": datetime.now().isoformat()
            }
            
            await self._emit_status(workflow_id, "workflow", "failed", error_result)
            return error_result
    
    async def _execute_agent_step(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        step_number: int,
        total_steps: int
    ) -> Any:
        """
        Execute a single agent step with status updates.
        
        Args:
            agent_name: Name of agent to execute
            input_data: Input data for agent
            step_number: Current step number
            total_steps: Total number of steps
            
        Returns:
            Agent result
        """
        workflow_id = self.state.get("workflow_id", "unknown")
        
        # Send "running" status
        await self._emit_status(
            workflow_id,
            agent_name,
            "running",
            {
                "step": step_number,
                "total_steps": total_steps,
                "message": f"Executing {agent_name}..."
            }
        )
        
        # Execute agent
        agent = self.agents[agent_name]
        result = await agent.execute(input_data, context=self.state)
        
        # Send "completed" status with result
        await self._emit_status(
            workflow_id,
            agent_name,
            "completed",
            {
                "step": step_number,
                "total_steps": total_steps,
                "result": {
                    "output": result.output,
                    "reasoning": result.reasoning,
                    "confidence": result.confidence,
                    "cost_usd": result.cost_usd,
                    "latency_ms": result.latency_ms,
                    "tokens_used": result.tokens_used
                }
            }
        )
        
        return result
    
    async def _emit_status(
        self,
        workflow_id: str,
        agent_name: str,
        status: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Emit status update via websocket callback.
        
        Args:
            workflow_id: Workflow ID
            agent_name: Agent name
            status: Status (running, completed, failed)
            data: Additional data to send
        """
        if self.websocket_callback:
            update = {
                "workflow_id": workflow_id,
                "agent": agent_name,
                "status": status,
                "data": data,
                "timestamp": time.time()
            }
            
            try:
                await self.websocket_callback(update)
            except Exception as e:
                # Don't let websocket errors break workflow
                print(f"WebSocket error: {e}")
    
    def get_state(self) -> Dict[str, Any]:
        """Get current workflow state."""
        return self.state.copy()
    
    def reset_state(self) -> None:
        """Reset workflow state."""
        self.state = {}
