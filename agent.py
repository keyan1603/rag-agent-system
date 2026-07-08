"""
RAG-Powered Agentic AI Agent

This module implements the complete RAG + Agentic Loop system.

The agent:
1. Retrieves relevant documentation for user queries
2. Uses multi-turn conversation to reason about problems
3. Calls tools to execute actions
4. Stores results in memory for continued reasoning
5. Provides grounded, actionable answers
"""

import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import google.genai as genai


load_dotenv()


class RAGAgentWithLoop:
    """
    RAG-powered agentic AI with multi-turn loops.
    
    This agent combines:
    - RAG (Retrieval-Augmented Generation) for grounded knowledge
    - Agentic loops (tool calling, reasoning, iteration)
    - Multi-turn conversation memory
    """
    
    def __init__(self, retriever, tool_registry, knowledge_base):
        """
        Initialize the RAG-powered agentic AI.
        
        Args:
            retriever: RAGRetriever instance for semantic search
            tool_registry: Dictionary of available tools
            knowledge_base: Original knowledge base documents
        """
        self.retriever = retriever
        self.tool_registry = tool_registry
        self.knowledge_base = knowledge_base
        self.conversation_history: List[Dict[str, str]] = []
        
        # Initialize Gemini client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set. "
                "Get your API key from https://aistudio.google.com/"
            )
        self.client = genai.Client(api_key=api_key)
        
    def _build_rag_context(self, query: str) -> str:
        """
        Retrieve relevant documents and build context string.
        
        This context is added to the agent's prompt, grounding its
        reasoning in actual documentation rather than training data.
        
        Args:
            query: User question to search for
            
        Returns:
            Formatted context string with retrieved documents
        """
        retrieved_docs = self.retriever.retrieve(query, top_k=3)
        
        if not retrieved_docs:
            return "No relevant documentation found for this query."
        
        context = "📚 **Relevant Documentation:**\n\n"
        for i, result in enumerate(retrieved_docs, 1):
            doc = result["document"]
            score = result["relevance_score"]
            context += f"{i}. **{doc['title']}** (relevance: {score:.2f})\n"
            context += f"{doc['content']}\n\n"
        
        return context
    
    def _create_tool_declarations(self) -> List[Dict[str, Any]]:
        """
        Create Gemini tool declarations from tool registry.
        
        Converts internal tool definitions to format expected by google-genai API.
        
        Returns:
            List of tool declarations in Gemini format
        """
        tools = []
        
        for tool_name, tool_info in self.tool_registry.items():
            schema = tool_info["input_schema"].model_json_schema()
            
            # Convert Pydantic schema to Gemini function declaration format
            properties_dict = {}
            for prop, details in schema.get("properties", {}).items():
                detail_type = details.get("type")
                if detail_type == "boolean":
                    p_type = "BOOLEAN"
                elif detail_type == "integer":
                    p_type = "INTEGER"
                elif detail_type == "number":
                    p_type = "NUMBER"
                elif detail_type == "array":
                    p_type = "ARRAY"
                elif detail_type == "object":
                    p_type = "OBJECT"
                else:
                    p_type = "STRING"
                
                property_schema = {
                    "type": p_type,
                    "description": details.get("description", "")
                }
                
                if detail_type == "array":
                    items_type = details.get("items", {}).get("type", "string")
                    if items_type == "boolean":
                        items_type = "BOOLEAN"
                    elif items_type == "integer":
                        items_type = "INTEGER"
                    elif items_type == "number":
                        items_type = "NUMBER"
                    elif items_type == "array":
                        items_type = "ARRAY"
                    elif items_type == "object":
                        items_type = "OBJECT"
                    else:
                        items_type = "STRING"
                    property_schema["items"] = {"type": items_type}
                
                properties_dict[prop] = property_schema
            
            function_decl = genai.types.FunctionDeclaration(
                name=tool_name,
                description=tool_info["description"],
                parameters={
                    "type": "OBJECT",
                    "properties": properties_dict,
                    "required": schema.get("required", [])
                }
            )
            tools.append(genai.types.Tool(functionDeclarations=[function_decl]))
        
        return tools
    
    def run(self, user_query: str, max_iterations: int = 10) -> str:
        """
        Run the RAG-powered agentic loop.
        
        Main entry point. The loop:
        1. Retrieves documents from knowledge base
        2. Initializes agent with retrieved context
        3. Loops: agent thinks → calls tools → stores results
        4. Exits when agent decides it has the answer
        
        Args:
            user_query: User's question or request
            max_iterations: Maximum loop iterations (safety limit)
            
        Returns:
            Final answer from the agent
        """
        print(f"\n{'='*70}")
        print(f"User Query: {user_query}")
        print(f"{'='*70}\n")
        
        # Step 1: Retrieve relevant documents
        print("🔍 Retrieving relevant documentation...\n")
        rag_context = self._build_rag_context(user_query)
        print(rag_context)
        
        # Step 2: Initialize conversation with context
        system_prompt = f"""You are a helpful deployment assistant with expertise in DevOps, deployment strategies, and system monitoring.

You have access to the company's deployment documentation and best practices.
When answering questions, reference the documentation below and follow recommended procedures.

{rag_context}

When the user asks about deployment or processes:
1. Reference the relevant documentation
2. Call tools to execute recommended steps
3. Monitor results from tool calls
4. Provide comprehensive guidance based on actual tool results

Be conversational but precise. Always follow the documented procedures.
If something goes wrong, suggest remediation steps based on the documentation."""

        # Build messages for new API format
        # Preserve previous conversation history by default. Only seed the system
        # prompt once when history is empty so multi-turn conversations persist.
        if not self.conversation_history:
            # use 'model' internally (will be mapped to Gemini's MODEL role)
            self.conversation_history = [
                {
                    "role": "model",
                    "content": system_prompt
                }
            ]
        # Append the new user query as the next turn
        self.conversation_history.append({
            "role": "user",
            "content": user_query
        })
        
        # Get tool declarations
        tools = self._create_tool_declarations()
        
        # Step 3: The agentic loop
        iteration = 0
        final_answer = None
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n[Iteration {iteration}] Agent thinking...")
            
            # Call Gemini API with tools
            try:
                contents = []
                # Build Content objects and normalize roles to Gemini's expected literals
                for message in self.conversation_history:
                    role_literal = message.get("role", "user").upper()
                    if role_literal not in ("USER", "MODEL"):
                        role_literal = "USER"
                    contents.append(
                        genai.types.Content(
                            role=role_literal,
                            parts=[genai.types.Part(text=message["content"])]
                        )
                    )
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config={
                        "temperature": 0.7,
                        "max_output_tokens": 2048,
                        "tools": tools
                    }
                )
            except Exception as e:
                print(f"❌ API Error: {e}")
                print("   Make sure GEMINI_API_KEY is set correctly")
                return f"Error occurred during agent execution: {str(e)}"
            
            # Extract response content and tool calls
            response_text = ""
            tool_called = False
            tool_results = []
            candidate = None
            if getattr(response, "candidates", None):
                candidate = response.candidates[0]
                content = getattr(candidate, "content", None)
                if content and getattr(content, "parts", None):
                    text_parts = []
                    for part in content.parts:
                        if getattr(part, "function_call", None):
                            tool_called = True
                            tool_call = part.function_call
                            tool_name = tool_call.name
                            args = tool_call.args or {}
                            
                            print(f"🔧 Tool Call: {tool_name}")
                            print(f"   Parameters: {args}")
                            
                            # Execute the tool
                            try:
                                if tool_name in self.tool_registry:
                                    input_schema = self.tool_registry[tool_name]["input_schema"]
                                    validated_input = input_schema(**args)
                                    tool_function = self.tool_registry[tool_name]["function"]
                                    result = tool_function(**validated_input.model_dump())
                                    
                                    print(f"   ✓ Result: {result}")
                                    tool_results.append({
                                        "tool_name": tool_name,
                                        "result": result
                                    })
                                else:
                                    raise ValueError(f"Unknown tool: {tool_name}")
                            except Exception as e:
                                print(f"   ✗ Error: {e}")
                                tool_results.append({
                                    "tool_name": tool_name,
                                    "result": f"Error: {str(e)}"
                                })
                        elif getattr(part, "text", None):
                            text_parts.append(part.text)
                    response_text = "\n".join(text_parts).strip()
                else:
                    response_text = getattr(candidate, "content", "") or ""
            else:
                response_text = getattr(response, "text", "") or ""
            
            # Add model response to history
            self.conversation_history.append({
                "role": "model",
                "content": response_text
            })

            # If no tool was called, model has the final answer
            if not tool_called:
                print(f"\n✅ Agent Finished")
                print(f"\nFinal Answer:\n{'-'*70}")
                print(response_text if response_text else "No response generated")
                print(f"{'-'*70}\n")
                final_answer = response_text
                break
            
            # Store tool results in conversation history for next iteration
            results_text = "\nTool Results:\n"
            for tool_result in tool_results:
                results_text += f"- {tool_result['tool_name']}: {tool_result['result']}\n"
            
            self.conversation_history.append({
                "role": "user",
                "content": results_text
            })
            
            print(f"📝 Results stored in memory. Agent will continue...\n")
        
        if iteration >= max_iterations:
            print(f"\n⚠️  Max iterations ({max_iterations}) reached")
            return "Max iterations reached. Agent did not complete."
        
        return final_answer or "No answer generated"
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Useful for debugging and understanding the agent's reasoning.
        
        Returns:
            List of conversation turns
        """
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history for next conversation."""
        self.conversation_history = []


def test_agent(retriever, tool_registry, knowledge_base):
    """
    Test the agent with sample queries.
    
    Args:
        retriever: RAGRetriever instance
        tool_registry: Tool registry
        knowledge_base: Knowledge base documents
    """
    print("\n" + "="*70)
    print("Testing RAG + Agentic Agent")
    print("="*70)
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  GEMINI_API_KEY not set!")
        print("Set it with: export GEMINI_API_KEY=your_key_here")
        print("Get your key from: https://aistudio.google.com/")
        return
    
    agent = RAGAgentWithLoop(retriever, tool_registry, knowledge_base)
    
    # Test queries
    test_queries = [
        "I need to deploy version 2.5.0. What's the process?",
        "Deploy to staging and verify it works",
    ]
    
    for query in test_queries:
        result = agent.run(query)
        print(f"\n{'='*70}\n")
        agent.clear_history()


if __name__ == "__main__":
    # Test when run directly
    from knowledge_base import KNOWLEDGE_BASE
    from retriever import RAGRetriever
    from tools import tool_registry
    
    retriever = RAGRetriever(KNOWLEDGE_BASE)
    test_agent(retriever, tool_registry, KNOWLEDGE_BASE)
