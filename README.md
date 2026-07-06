# RAG-Powered Agentic AI Agent

A production-ready deployment assistant that combines Retrieval-Augmented Generation (RAG) with agentic AI loops for intelligent multi-turn problem solving.

## 🎯 What This Does

This system enables an AI agent to:

1. **Retrieve** relevant documentation from your knowledge base
2. **Reason** about complex multi-step problems
3. **Call tools** to execute actions (run tests, deploy, monitor)
4. **Learn** from results and iterate until the problem is solved
5. **Ground** all answers in your actual documentation

Perfect for deployment assistance, troubleshooting, and operational guidance.

## 📋 Features

- ✅ **RAG (Retrieval-Augmented Generation)** - Ground answers in your documentation
- ✅ **Agentic Loops** - Multi-turn reasoning with tool calling
- ✅ **Tool Integration** - Execute real actions via predefined tools
- ✅ **Conversation Memory** - Maintain context across iterations
- ✅ **REST API** - Easy integration with other systems
- ✅ **Kubernetes Ready** - Production deployment manifests included
- ✅ **Docker Support** - Container everything easily
- ✅ **Extensible** - Add more tools and documents easily

## 🚀 Quick Start

### 1. Get Your API Key

Visit [Google AI Studio](https://aistudio.google.com/) and get a free Gemini API key.

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/rag-agent-system.git
cd rag-agent-system

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Run It

**Option A: Interactive Mode**
```bash
export GEMINI_API_KEY=your_key_here
python main.py

# Then type your questions:
# > Deploy version 2.5.0 and verify it works
```

**Option B: Command Line**
```bash
export GEMINI_API_KEY=your_key_here
python main.py "Deploy version 2.5.0"
```

**Option C: REST API**
```bash
export GEMINI_API_KEY=your_key_here
uvicorn api:app --reload

# Visit: http://localhost:8000/docs
# Or test with curl:
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Deploy version 2.5.0"}'
```

## 📁 Project Structure

```
rag-agent-system/
├── knowledge_base.py        # Your documentation database
├── retriever.py             # RAG retrieval logic
├── tools.py                 # Tool definitions and implementations
├── agent.py                 # RAG + Agentic loop implementation
├── main.py                  # Standalone CLI entry point
├── api.py                   # FastAPI REST service
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container configuration
├── deployment.yaml          # Kubernetes manifests
├── .env.example             # Environment configuration template
└── README.md               # This file
```

## 🔧 How It Works

### Architecture

```
User Query
    ↓
[RAG Retriever] → Search knowledge base
    ↓
[Agent + Tools] → Reason & execute
    ↓
[Conversation Memory] → Store results
    ↓
[Next Iteration] → Continue reasoning
    ↓
Final Answer (grounded in your docs)
```

### Example Workflow

**User:** "Deploy version 2.5.0 to staging"

**Agent:**
1. Retrieves deployment documentation
2. Thinks: "Docs say I need to run tests first"
3. Calls: `run_tests(test_scope="all")`
4. Sees result: "✓ All 189 tests passed"
5. Thinks: "Now I should build artifacts"
6. Calls: `build_artifacts(version="2.5.0")`
7. And so on...
8. Finally: Returns comprehensive deployment report

## 🛠️ Customization

### Add Your Knowledge Base

Edit `knowledge_base.py`:

```python
KNOWLEDGE_BASE = [
    {
        "id": "doc_1",
        "title": "Your Document Title",
        "content": "Your documentation content..."
    },
    # Add more documents...
]
```

### Add New Tools

Edit `tools.py`:

```python
class YourToolInput(BaseModel):
    """Input schema for your tool."""
    param1: str = Field(description="...")

def your_tool(param1: str) -> str:
    """Implement your tool."""
    # Do something useful
    return "result"

# Register in tool_registry
tool_registry["your_tool"] = {
    "function": your_tool,
    "input_schema": YourToolInput,
    "description": "What your tool does"
}
```

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t rag-agent:1.0.0 .
```

### Run Container

```bash
docker run -e GEMINI_API_KEY=your_key \
  -p 8000:8000 \
  rag-agent:1.0.0
```

## ☸️ Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (GKE, EKS, AKS, etc.)
- `kubectl` configured
- Docker image pushed to your registry

### Deploy

```bash
# Set your image
sed -i 's|gcr.io/myproject/rag-agent:1.0.0|your-registry/rag-agent:1.0.0|g' deployment.yaml

# Create secret with API key
kubectl create secret generic gemini-secrets \
  --from-literal=api-key=YOUR_API_KEY

# Deploy
kubectl apply -f deployment.yaml

# Check status
kubectl get pods -l app=rag-agent
kubectl logs deployment/rag-agent -f
kubectl get svc rag-agent-service
```

## 📚 API Reference

### Query Endpoint

**POST** `/query`

Request:
```json
{
  "query": "Your question here",
  "max_iterations": 10
}
```

Response:
```json
{
  "query": "Your question here",
  "answer": "Agent's response",
  "status": "success"
}
```

### Health Check

**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "message": "Agent service is running"
}
```

### Documentation Info

**GET** `/docs-info`

Returns information about available tools and knowledge base documents.

## 🧪 Testing

### Test Components

```bash
# Test retriever
python -c "from retriever import test_retriever; from knowledge_base import KNOWLEDGE_BASE; test_retriever(KNOWLEDGE_BASE)"

# Test tools
python -c "from tools import test_tools; test_tools()"

# Test agent (requires GEMINI_API_KEY)
python agent.py
```

## 🔍 Debugging

### View Agent Reasoning

The agent prints its thinking at each iteration:

```
[Iteration 1] Agent thinking...
🔍 Retrieving relevant documentation...
🔧 Tool Call: run_tests
   Parameters: {'test_scope': 'all'}
   ✓ Result: ✓ Unit tests: 147 passed...
📝 Results stored in memory. Agent will continue...
```

### Check Conversation History

```python
from main import agent

result = agent.run("your query")
print(agent.get_conversation_history())
```

## 📊 Performance Tips

1. **Knowledge Base**: Keep documents focused and well-organized
2. **Tool Descriptions**: Clear descriptions help the agent choose correctly
3. **Max Iterations**: Set appropriate limits (default: 10)
4. **Caching**: Implement retrieval caching for frequent queries
5. **Monitoring**: Track agent accuracy and tool success rates

## 🐛 Troubleshooting

### "GEMINI_API_KEY not set"

```bash
export GEMINI_API_KEY=your_key_here
```

### Pods not starting in Kubernetes

```bash
kubectl describe pod POD_NAME
kubectl logs POD_NAME
```

### API returns 500 error

Check logs:
```bash
kubectl logs deployment/rag-agent -f
```

## 🚀 Next Steps

1. **Expand Knowledge Base** - Add your documentation
2. **Add More Tools** - Integrate with your systems
3. **Production Setup** - Deploy to Kubernetes
4. **Monitor** - Add Prometheus metrics
5. **Extend** - Build multi-agent systems

## 📝 Example Queries

- "Deploy version 2.5.0 to staging"
- "What should I check before deploying?"
- "Deploy to production and monitor for issues"
- "What do I do if deployment fails?"
- "Run tests and tell me if everything is ready"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add improvements or tools
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🎓 Learn More

- [RAG + Agentic Loops Blog Post](../rag_agentic_blog.md)
- [Google Gemini API Docs](https://ai.google.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

## 💬 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the blog post for architecture details
3. Open an issue on GitHub

---

**Built with ❤️ for intelligent deployment assistance**
