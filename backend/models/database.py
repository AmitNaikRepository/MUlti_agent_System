"""
Database models and setup for metrics storage.
Uses SQLite for simplicity (can be upgraded to PostgreSQL for production).
"""
import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pathlib import Path

# Create data directory if it doesn't exist
Path("./data").mkdir(exist_ok=True)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/metrics.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class WorkflowExecution(Base):
    """Table for storing workflow execution records."""
    __tablename__ = "workflow_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, unique=True, index=True)
    status = Column(String)  # completed, failed
    user_input = Column(Text)
    category = Column(String)
    urgency = Column(String)
    final_output = Column(Text)
    
    # Metrics
    total_cost_usd = Column(Float)
    total_latency_ms = Column(Integer)
    total_tokens = Column(Integer)
    avg_confidence = Column(Float)
    agents_used = Column(Integer)
    
    # Metadata
    workflow_data = Column(JSON)  # Full workflow result as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "status": self.status,
            "user_input": self.user_input,
            "category": self.category,
            "urgency": self.urgency,
            "final_output": self.final_output,
            "total_cost_usd": self.total_cost_usd,
            "total_latency_ms": self.total_latency_ms,
            "total_tokens": self.total_tokens,
            "avg_confidence": self.avg_confidence,
            "agents_used": self.agents_used,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class AgentMetrics(Base):
    """Table for storing individual agent performance metrics."""
    __tablename__ = "agent_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, index=True)
    agent_name = Column(String, index=True)
    
    # Performance metrics
    latency_ms = Column(Integer)
    cost_usd = Column(Float)
    tokens_used = Column(Integer)
    confidence = Column(Float)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
