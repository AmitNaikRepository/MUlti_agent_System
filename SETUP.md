# 📋 SETUP Guide

Detailed setup and deployment instructions for the Multi-Agent Orchestration System.

## 🔧 Local Development Setup

### Step 1: Prerequisites

Ensure you have the following installed:

```bash
# Check Python version (3.10+ required)
python --version

# Check Node.js version (18+ required)
node --version
npm --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/multi-agent-system.git
cd multi-agent-system
```

### Step 3: Backend Setup

1. **Create virtual environment** (recommended)
```bash
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
GROQ_API_KEY=your_groq_api_key_here  # Get from https://console.groq.com/
```

4. **Initialize database**
```bash
# Database will be created automatically on first run
# Located at: ./data/metrics.db
```

5. **Test backend**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` to see API documentation.

### Step 4: Frontend Setup

1. **Navigate to frontend**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start dev server**
```bash
npm run dev
```

The frontend will start at `http://localhost:3000`.

## 🎯 Usage

### Running the Full Stack

You need **two terminal windows**:

**Terminal 1 (Backend):**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Then open `http://localhost:3000` in your browser.

### Testing with Sample Data

The system comes with pre-loaded sample tickets in `data/sample_tickets.json`:

1. Click any sample ticket button
2. Click "Execute Workflow"
3. Watch the real-time execution

## 🔌 API Key Setup

### Getting a Groq API Key

1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up / Log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and paste it in your `.env` file

**Note**: Groq offers a generous free tier. No credit card required to start!

### Optional: OpenAI Key (for comparison)

If you want to test the single LLM comparison feature:
```bash
OPENAI_API_KEY=your_openai_key_here
```

## 🗂️ Database

The system uses SQLite for simplicity:

- **Location**: `./data/metrics.db`
- **Tables**: `workflow_executions`, `agent_metrics`
- **Initialization**: Automatic on first run

### Viewing Database

```bash
sqlite3 data/metrics.db
```

```sql
-- View all workflows
SELECT * FROM workflow_executions LIMIT 10;

-- View agent performance
SELECT agent_name, AVG(latency_ms), AVG(cost_usd) 
FROM agent_metrics 
GROUP BY agent_name;
```

## 📝 Configuration Options

### Backend Configuration (`.env`)

```bash
# Required
GROQ_API_KEY=your_key_here

# Optional
OPENAI_API_KEY=your_key_here
DATABASE_URL=sqlite:///./data/metrics.db
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development

# Redis (optional, for distributed systems)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_ENABLED=false
```

### Frontend Configuration

Create `frontend/.env` (optional):
```bash
VITE_API_URL=http://localhost:8000/api
```

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'backend'`
```bash
# Make sure you're in the root directory and run:
python -m uvicorn backend.main:app --reload
```

**Issue**: Database errors
```bash
# Delete and recreate database
rm data/metrics.db
# Restart backend (will recreate automatically)
```

**Issue**: Groq API errors
```bash
# Check your API key is valid
# Check you haven't exceeded rate limits
# Groq free tier limits: ~30 requests/minute
```

### Frontend Issues

**Issue**: `Cannot connect to backend`
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`

**Issue**: Components not rendering
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Issue**: WebSocket connection failed
- Check that backend WebSocket endpoint is accessible
- Browser console will show connection errors

## 🚀 Production Deployment

### Backend Deployment (e.g., Render, Railway, Fly.io)

1. **Set environment variables** in your hosting platform
2. **Use production ASGI server**:
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

3. **Use PostgreSQL** instead of SQLite:
```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### Frontend Deployment (e.g., Vercel, Netlify)

1. **Build the frontend**:
```bash
cd frontend
npm run build
```

2. **Set environment variable**:
```bash
VITE_API_URL=https://your-backend-url.com/api
```

3. **Deploy** the `frontend/dist` folder

### Docker Deployment (Future Enhancement)

```dockerfile
# Dockerfile example (not included in current version)
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ ./backend/
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 Adding New Agents

To add a new specialized agent:

1. **Create agent file**: `backend/agents/my_new_agent.py`
```python
from .base_agent import BaseAgent, AgentConfig

class MyNewAgent(BaseAgent):
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        config = AgentConfig(
            name="MyNewAgent",
            model=model,
            temperature=0.7,
            max_tokens=1000,
            system_prompt="Your agent's system prompt here..."
        )
        super().__init__(config)
    
    def _build_prompt(self, input_data, context):
        return f"Your prompt template using {input_data} and {context}"
```

2. **Update orchestrator**: Add to `backend/agents/orchestrator.py`
```python
self.agents["my_new_agent"] = MyNewAgent()
```

3. **Update frontend**: Add node to `WorkflowCanvas.tsx`

## 🧪 Testing

### Backend Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/load_test.py
```

## 📈 Monitoring

### Metrics to Monitor

- **Cost per workflow**: Track in dashboard
- **Latency by agent**: Identify bottlenecks
- **Success rate**: Percentage of completed workflows
- **QA scores**: Average quality scores

### Logging

Logs are output to console. For production:
```python
# Use structured logging
import structlog
logger = structlog.get_logger()
```

## 🔐 Security

### Production Checklist

- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/TLS
- [ ] Add rate limiting
- [ ] Implement authentication if needed
- [ ] Sanitize user inputs
- [ ] Use CORS properly
- [ ] Keep dependencies updated

## 💡 Tips & Best Practices

1. **Cost Management**: Monitor Groq API usage carefully
2. **Error Handling**: Agents can fail; workflow should continue
3. **Prompt Engineering**: Iterate on agent prompts for better results
4. **Caching**: Consider caching common queries
5. **Monitoring**: Set up alerts for high costs or errors

## 📚 Additional Resources

- [Groq Documentation](https://console.groq.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Flow Documentation](https://reactflow.dev/)
- [Multi-Agent Systems Guide](https://python.langchain.com/docs/concepts/multiagency/)

## 🆘 Getting Help

If you encounter issues:

1. Check this SETUP guide
2. Review error logs in console
3. Check API documentation at `/docs`
4. Review sample code in `data/sample_tickets.json`

---

Happy coding! 🚀
