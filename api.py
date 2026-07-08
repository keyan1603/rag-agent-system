"""
FastAPI Service for RAG-Powered Agent

This module exposes the agent as a REST API.

Usage:
    uvicorn api:app --reload
    
Then visit:
    http://localhost:8000/docs  (interactive API docs)
    
Example request:
    curl -X POST http://localhost:8000/query \
      -H "Content-Type: application/json" \
      -d '{"query": "Deploy version 2.5.0", "max_iterations": 10}'
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from knowledge_base import KNOWLEDGE_BASE
from retriever import RAGRetriever
from agent import RAGAgentWithLoop
from tools import tool_registry


load_dotenv()


# ============================================================================
# Request/Response Models
# ============================================================================

class QueryRequest(BaseModel):
    """Request model for agent queries."""
    query: str = Field(..., description="The user's question or request")
    max_iterations: int = Field(
        default=10,
        description="Maximum iterations for the agent loop",
        ge=1,
        le=20
    )


class QueryResponse(BaseModel):
    """Response model for agent queries."""
    query: str = Field(..., description="Original query")
    answer: str = Field(..., description="Agent's response")
    status: str = Field(default="success", description="Execution status")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(default="healthy")
    message: str = Field(default="Agent service is running")


class DocumentInfo(BaseModel):
    """Information about a knowledge base document."""
    id: str
    title: str


class DocsResponse(BaseModel):
    """Documentation info response."""
    tools: list = Field(description="Available tools")
    knowledge_base_docs: int = Field(description="Number of knowledge base documents")
    available_documents: list[DocumentInfo] = Field(description="List of documents")


# ============================================================================
# FastAPI App Setup
# ============================================================================

app = FastAPI(
    title="RAG-Powered Agent API",
    description="API for the RAG + Agentic AI deployment assistant",
    version="1.0.0"
)

# Initialize agent on startup
print("Initializing RAG Agent...")
retriever = RAGRetriever(KNOWLEDGE_BASE)
agent = RAGAgentWithLoop(
    retriever=retriever,
    tool_registry=tool_registry,
    knowledge_base=KNOWLEDGE_BASE
)
print("✓ Agent initialized successfully")


# ============================================================================
# API Endpoints
# ============================================================================

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest) -> QueryResponse:
    """
    Process a user query through the RAG-powered agent.
    
    The agent:
    1. Retrieves relevant documentation
    2. Reasons about the query
    3. Calls tools to execute actions
    4. Returns a comprehensive answer
    
    Args:
        request: QueryRequest with query and optional max_iterations
        
    Returns:
        QueryResponse with answer and status
        
    Raises:
        HTTPException: If query processing fails
    """
    try:
        answer = agent.run(
            request.query,
            max_iterations=request.max_iterations
        )
        # Preserve conversation history by default so follow-up HTTP requests
        # can continue the same session. If you want per-request isolation,
        # call `agent.clear_history()` explicitly or enable it via a flag.
        
        return QueryResponse(
            query=request.query,
            answer=answer or "No answer generated",
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Verifies the agent service is running and responsive.
    
    Returns:
        HealthResponse with status
    """
    try:
        # Quick verification that agent is initialized
        if agent:
            return HealthResponse(
                status="healthy",
                message="Agent service is running"
            )
        else:
            return HealthResponse(
                status="unhealthy",
                message="Agent not initialized"
            )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {str(e)}"
        )


@app.get("/docs-info", response_model=DocsResponse)
async def get_documentation() -> DocsResponse:
    """
    Get information about available tools and knowledge base.
    
    This helps clients understand what the agent can do.
    
    Returns:
        DocsResponse with available tools and documents
    """
    try:
        return DocsResponse(
            tools=list(tool_registry.keys()),
            knowledge_base_docs=len(KNOWLEDGE_BASE),
            available_documents=[
                DocumentInfo(id=doc["id"], title=doc["title"])
                for doc in KNOWLEDGE_BASE
            ]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving documentation: {str(e)}"
        )


@app.get("/tools")
async def list_tools():
    """
    List all available tools.
    
    Returns:
        Dictionary of tools with descriptions
    """
    tools_info = {}
    for tool_name, tool_info in tool_registry.items():
        tools_info[tool_name] = {
            "description": tool_info.get("description", ""),
            "input_schema": tool_info["input_schema"].model_json_schema()
        }
    return tools_info


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        Information about the API
    """
    return {
        "name": "RAG-Powered Agent API",
        "version": "1.0.0",
        "description": "Deployment assistant using RAG + Agentic AI loops",
        "endpoints": {
            "query": {
                "method": "POST",
                "path": "/query",
                "description": "Process a query through the agent"
            },
            "health": {
                "method": "GET",
                "path": "/health",
                "description": "Health check"
            },
            "docs_info": {
                "method": "GET",
                "path": "/docs-info",
                "description": "Get information about tools and knowledge base"
            },
            "tools": {
                "method": "GET",
                "path": "/tools",
                "description": "List available tools"
            },
            "docs": {
                "method": "GET",
                "path": "/docs",
                "description": "Interactive API documentation (Swagger UI)"
            },
            "openapi": {
                "method": "GET",
                "path": "/openapi.json",
                "description": "OpenAPI schema"
            }
        }
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    return {
        "error": str(exc),
        "status_code": 500
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
