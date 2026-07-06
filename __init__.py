"""
RAG-Powered Agentic AI Agent

A complete system combining Retrieval-Augmented Generation (RAG) with agentic AI loops
for intelligent multi-turn problem solving and deployment assistance.

Main components:
- knowledge_base: Your documentation database
- retriever: RAG retrieval using semantic search
- tools: Actions the agent can take
- agent: The RAG + Agentic loop implementation
- api: FastAPI REST wrapper
- main: Standalone CLI interface

Example usage:
    from agent import RAGAgentWithLoop
    from knowledge_base import KNOWLEDGE_BASE
    from retriever import RAGRetriever
    from tools import tool_registry
    
    retriever = RAGRetriever(KNOWLEDGE_BASE)
    agent = RAGAgentWithLoop(retriever, tool_registry, KNOWLEDGE_BASE)
    
    result = agent.run("Deploy version 2.5.0")
    print(result)
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "RAG-Powered Agentic AI for intelligent problem solving"

from knowledge_base import KNOWLEDGE_BASE, get_knowledge_base
from retriever import RAGRetriever
from tools import tool_registry, get_tool_registry
from agent import RAGAgentWithLoop

__all__ = [
    "KNOWLEDGE_BASE",
    "get_knowledge_base",
    "RAGRetriever",
    "tool_registry",
    "get_tool_registry",
    "RAGAgentWithLoop",
]
