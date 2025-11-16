"""
Base Agent Class for Multi-Agent Orchestration System.
Provides common functionality for all specialized agents.
"""
import os
import time
import json
import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from groq import Groq


class AgentConfig(BaseModel):
    """Configuration for an agent."""
    name: str
    model: str  # Groq model to use
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: str
    
    class Config:
        frozen = True  # Make immutable


class AgentResult(BaseModel):
    """Result from an agent execution."""
    agent_name: str
    output: str
    reasoning: str  # Why agent made this decision
    confidence: float = Field(ge=0.0, le=1.0)  # 0-1
    cost_usd: float
    latency_ms: int
    tokens_used: int
    raw_response: Optional[str] = None
    
    class Config:
        json_encoders = {
            float: lambda v: round(v, 6)
        }


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    
    Each agent:
    - Has a specific role and system prompt
    - Executes tasks using Groq LLM
    - Tracks metrics (cost, latency, tokens)
    - Returns structured results
    """
    
    def __init__(self, config: AgentConfig):
        """
        Initialize the agent.
        
        Args:
            config: Agent configuration including name, model, and system prompt
        """
        self.config = config
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
    async def execute(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> AgentResult:
        """
        Execute the agent's task and return structured result.
        
        Args:
            input_data: Input data specific to this agent's task
            context: Shared context from previous agents in the workflow
            
        Returns:
            AgentResult with output, metrics, and metadata
        """
        start_time = time.time()
        
        try:
            # Build prompt with context
            prompt = self._build_prompt(input_data, context or {})
            
            # Call Groq API
            response = self.groq_client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self.config.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            latency = (time.time() - start_time) * 1000
            
            # Parse response
            output = response.choices[0].message.content
            tokens = response.usage.total_tokens
            cost = self._calculate_cost(tokens)
            
            # Extract reasoning and confidence from output
            reasoning = self._extract_reasoning(output)
            confidence = self._calculate_confidence(output, response)
            
            return AgentResult(
                agent_name=self.config.name,
                output=output,
                reasoning=reasoning,
                confidence=confidence,
                cost_usd=cost,
                latency_ms=int(latency),
                tokens_used=tokens,
                raw_response=output
            )
            
        except Exception as e:
            # Handle errors gracefully
            latency = (time.time() - start_time) * 1000
            error_msg = f"Error in {self.config.name}: {str(e)}"
            
            return AgentResult(
                agent_name=self.config.name,
                output=error_msg,
                reasoning=f"Agent failed: {type(e).__name__}",
                confidence=0.0,
                cost_usd=0.0,
                latency_ms=int(latency),
                tokens_used=0,
                raw_response=error_msg
            )
    
    @abstractmethod
    def _build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Build the prompt for this agent.
        Each agent implements its own prompt engineering.
        
        Args:
            input_data: Input data specific to this agent
            context: Shared context from workflow
            
        Returns:
            Formatted prompt string
        """
        pass
    
    def _calculate_cost(self, tokens: int) -> float:
        """
        Calculate cost based on tokens and model.
        
        Args:
            tokens: Total tokens used
            
        Returns:
            Cost in USD
        """
        # Groq pricing (approximate - update based on actual pricing)
        cost_per_1m_tokens = {
            "llama-3.1-8b-instant": 0.05,
            "llama-3.1-70b-versatile": 0.59,
            "mixtral-8x7b-32768": 0.24,
            "gemma-7b-it": 0.07
        }
        
        rate = cost_per_1m_tokens.get(self.config.model, 0.10)
        return (tokens / 1_000_000) * rate
    
    def _extract_reasoning(self, output: str) -> str:
        """
        Extract reasoning from agent output.
        Looks for JSON 'reasoning' field or falls back to first sentence.
        
        Args:
            output: Agent output string
            
        Returns:
            Extracted reasoning
        """
        try:
            # Try to parse as JSON
            if output.strip().startswith('{'):
                data = json.loads(output)
                if 'reasoning' in data:
                    return data['reasoning']
        except json.JSONDecodeError:
            pass
        
        # Fallback: return first sentence or first 100 chars
        sentences = output.split('.')
        if sentences:
            return sentences[0].strip()[:100]
        
        return output[:100]
    
    def _calculate_confidence(self, output: str, response: Any) -> float:
        """
        Calculate confidence score for the agent's output.
        
        Args:
            output: Agent output string
            response: Raw Groq API response
            
        Returns:
            Confidence score between 0 and 1
        """
        try:
            # Try to extract confidence from JSON output
            if output.strip().startswith('{'):
                data = json.loads(output)
                if 'confidence' in data:
                    return float(data['confidence'])
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Heuristic: base confidence on response quality indicators
        confidence = 0.7  # Base confidence
        
        # Higher confidence for structured outputs
        if '{' in output and '}' in output:
            confidence += 0.1
        
        # Higher confidence for longer, detailed responses
        if len(output) > 200:
            confidence += 0.1
        
        # Cap at 0.95 for estimated confidence
        return min(confidence, 0.95)
    
    def _extract_json(self, output: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON from agent output.
        Handles cases where JSON is embedded in markdown or text.
        
        Args:
            output: Agent output string
            
        Returns:
            Parsed JSON dict or None
        """
        try:
            # Try direct parse
            return json.loads(output)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code block
        json_match = re.search(r'```json\s*(.*?)\s*```', output, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON object in text
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        return None
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.config.name}', model='{self.config.model}')"
