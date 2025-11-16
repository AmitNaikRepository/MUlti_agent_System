"""
Multi-Agent System - Specialized AI Agents for Customer Support.

This package contains:
- BaseAgent: Abstract base class for all agents
- ClassifierAgent: Categorizes customer requests
- ResearchAgent: Searches knowledge base for information
- ValidatorAgent: Validates requests against policies
- WriterAgent: Generates professional responses
- QAAgent: Reviews response quality
"""
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .classifier_agent import ClassifierAgent
from .research_agent import ResearchAgent
from .validator_agent import ValidatorAgent
from .writer_agent import WriterAgent
from .qa_agent import QAAgent

__all__ = [
    'BaseAgent',
    'AgentConfig',
    'AgentResult',
    'ClassifierAgent',
    'ResearchAgent',
    'ValidatorAgent',
    'WriterAgent',
    'QAAgent',
]
