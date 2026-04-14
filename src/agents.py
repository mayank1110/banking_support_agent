"""
LangGraph Agent Module
Defines the agentic workflow for customer support interactions.
"""

from typing import TypedDict, Optional, Dict, Any

from langgraph.graph import StateGraph, END

from .handlers import handle_feedback, handle_query


class AgentState(TypedDict):
    """State schema for the agent workflow."""
    
    input: str
    customer_name: Optional[str]
    classification: Optional[str]
    tool_name: Optional[str]
    tool_input: Optional[Dict[str, Any]]
    tool_output: Optional[Dict[str, Any]]
    answer: Optional[Dict[str, Any]]
    ticket_id: Optional[int]


def reason(state: AgentState) -> Dict[str, Any]:
    """
    Reasoning node: Classify input and determine which tool to use.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with classification and tool selection
    """
    from .classifier import hf_model_classify
    
    user_text = state.get("input", "")
    customer_name = state.get("customer_name", "Customer")
    
    # Classify intent
    classification = hf_model_classify(user_text)
    state["classification"] = classification

    # Route to appropriate tool
    if classification in ["Positive Feedback", "Negative Feedback"]:
        return {
            "tool_name": "feedback",
            "tool_input": {"message": user_text, "customer_name": customer_name},
        }
    elif classification == "Query":
        return {"tool_name": "query", "tool_input": {"message": user_text}}
    else:
        return {
            "answer": {
                "classification": classification,
                "response": "Unable to classify your request.",
                "ticket_id": None,
            }
        }


def tool_executor(state: AgentState) -> Dict[str, Any]:
    """
    Tool executor node: Execute the selected tool.
    
    Args:
        state: Current agent state with tool selection
        
    Returns:
        Updated state with tool output
    """
    tool_name = state.get("tool_name")
    tool_input = state.get("tool_input")

    if tool_name == "feedback":
        msg = tool_input["message"]
        cname = tool_input.get("customer_name", "Customer")
        classification, response, ticket_id = handle_feedback(msg, cname)
        return {
            "tool_output": {
                "classification": classification,
                "response": response,
                "ticket_id": ticket_id,
            }
        }
    elif tool_name == "query":
        msg = tool_input["message"]
        classification, response, ticket_id = handle_query(msg)
        return {
            "tool_output": {
                "classification": classification,
                "response": response,
                "ticket_id": ticket_id,
            }
        }
    else:
        return {
            "tool_output": {
                "classification": None,
                "response": "Unknown tool",
                "ticket_id": None,
            }
        }


def finalize(state: AgentState) -> Dict[str, Any]:
    """
    Finalize node: Prepare final response.
    
    Args:
        state: Current agent state with tool output
        
    Returns:
        Final answer in state
    """
    out = state.get("tool_output", {})
    classification = out.get("classification")
    response = out.get("response")
    ticket_id = out.get("ticket_id")
    
    return {
        "answer": {
            "classification": classification,
            "response": response,
            "ticket_id": ticket_id,
        }
    }


# Build the workflow graph
def build_graph() -> StateGraph:
    """
    Build and compile the LangGraph workflow.
    
    Returns:
        Compiled workflow graph
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("reason", reason)
    workflow.add_node("tool_executor", tool_executor)
    workflow.add_node("finalize", finalize)
    
    # Set entry point
    workflow.set_entry_point("reason")
    
    # Add conditional edges from reason node
    workflow.add_conditional_edges(
        "reason",
        lambda state: "tool" if state.get("tool_name") else "final",
        {"tool": "tool_executor", "final": END},
    )
    
    # Add edges
    workflow.add_edge("tool_executor", "finalize")
    workflow.add_edge("finalize", END)
    
    # Compile the graph
    return workflow.compile()


# Create global app instance
app = build_graph()


if __name__ == "__main__":
    # Test the agent
    test_cases = [
        {"input": "How do I activate my debit card", "customer_name": "Mayank"},
        {"input": "Thanks, that was helpful", "customer_name": "John"},
        {"input": "My card was declined and I need help", "customer_name": "Jane"},
        {"input": "What is the status of 123456", "customer_name": "Customer"},
    ]

    for test in test_cases:
        print(f"\nInput: {test['input']}")
        result = app.invoke(test)
        answer = result.get("answer", {})
        print(f"Classification: {answer.get('classification')}")
        print(f"Response: {answer.get('response')}")
        print(f"Ticket ID: {answer.get('ticket_id')}")
