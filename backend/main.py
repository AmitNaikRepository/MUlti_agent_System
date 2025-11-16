"""
Main FastAPI application for Multi-Agent Orchestration System.
Provides REST API and WebSocket endpoints for agent workflow execution.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from .api.routes import router
from .models.database import init_db

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Initializes database on startup.
    """
    # Startup
    print("🚀 Initializing Multi-Agent Orchestration System...")
    init_db()
    print("✅ Database initialized")
    print("✅ Agents ready")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Multi-Agent Orchestration System",
    description="Enterprise-level multi-agent AI system for customer support automation",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        os.getenv("FRONTEND_URL", "http://localhost:3000")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["workflows"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Multi-Agent Orchestration System",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "api": "/api"
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("BACKEND_PORT", 8000))
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  Multi-Agent Orchestration System                        ║
║  Enterprise Customer Support Automation                  ║
╠══════════════════════════════════════════════════════════╣
║  🌐 API Server: http://{host}:{port}                    
║  📚 API Docs:   http://{host}:{port}/docs               
║  🔌 WebSocket:  ws://{host}:{port}/api/ws               
╚══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
