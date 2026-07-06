"""
Main Entry Point

This script runs the RAG-powered agentic AI agent.

Usage:
    python main.py "Your question here"
    
Or for interactive mode:
    python main.py
"""

import sys
import os
from knowledge_base import KNOWLEDGE_BASE
from retriever import RAGRetriever
from tools import tool_registry
from agent import RAGAgentWithLoop


def main():
    """Main execution function."""
    
    print("\n" + "="*70)
    print("RAG-Powered Agentic AI Agent")
    print("="*70)
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("\n❌ Error: GEMINI_API_KEY environment variable not set!")
        print("\nTo use this agent, you need to:")
        print("1. Get a free API key from: https://aistudio.google.com/")
        print("2. Set it in your environment:")
        print("   export GEMINI_API_KEY=your_api_key_here")
        print("\nThen run this script again.")
        sys.exit(1)
    
    # Initialize components
    print("\n🔧 Initializing...")
    retriever = RAGRetriever(KNOWLEDGE_BASE)
    agent = RAGAgentWithLoop(retriever, tool_registry, KNOWLEDGE_BASE)
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        # Query provided as argument
        query = " ".join(sys.argv[1:])
        print(f"\n📝 Running with query: {query}\n")
        result = agent.run(query)
        sys.exit(0)
    
    # Interactive mode
    print("\n" + "="*70)
    print("Interactive Mode")
    print("="*70)
    print("\nExamples of questions you can ask:")
    print("  - 'I need to deploy version 2.5.0. What should I do?'")
    print("  - 'Deploy to staging and verify it works'")
    print("  - 'What should I check before deploying?'")
    print("  - 'What do I do if deployment fails?'")
    print("\nType 'exit' to quit\n")
    
    while True:
        try:
            query = input("You: ").strip()
            
            if query.lower() in ["exit", "quit", "bye"]:
                print("\nGoodbye! 👋\n")
                break
            
            if not query:
                continue
            
            # Run agent
            result = agent.run(query)
            
            # Clear history for next query
            agent.clear_history()
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            agent.clear_history()


if __name__ == "__main__":
    main()
