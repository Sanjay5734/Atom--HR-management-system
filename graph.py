# graph.py
from langgraph.checkpoint.memory import MemorySaver  # use in-memory
from langgraph.graph import StateGraph, END
from schemas import GraphState  # Import the updated GraphState
from nodes import Nodes
from typing import Literal

# Instantiate nodes
nodes = Nodes()

# Add memory checkpointer
memory_saver = MemorySaver()

# Define the workflow
workflow = StateGraph(GraphState)

# 1. Entry Point: Extract user query
workflow.add_node("getUserQuery", nodes.get_user_query)
workflow.set_entry_point("getUserQuery")

# 2. Check if it's a reply and fetch history if needed
workflow.add_node("checkIfReply", nodes.check_if_reply)
workflow.add_edge("getUserQuery", "checkIfReply")

# 3. Decide on RAG
workflow.add_node("decideEmailRag", nodes.decide_email_rag)
workflow.add_node("decideDocRag", nodes.decide_doc_rag)
workflow.add_edge("checkIfReply", "decideEmailRag")
# Run doc decision after email decision
workflow.add_edge("decideEmailRag", "decideDocRag")

# --- RAG PATHS ---
# 4. Conditional Email RAG path
workflow.add_node("generateEmailQuery", nodes.generate_email_query)
workflow.add_node("retrieveEmails", nodes.retrieve_emails)
workflow.add_edge("generateEmailQuery", "retrieveEmails")

# 5. Conditional Document RAG path
workflow.add_node("generateDocQuery", nodes.generate_doc_query)
workflow.add_node("retrieveDocs", nodes.retrieve_docs)
workflow.add_edge("generateDocQuery", "retrieveDocs")

# --- ROUTING LOGIC ---

# 6. Node where all potential context gathering finishes
# We need a single node to route FROM after all RAG is done or skipped.
# Let's create a simple pass-through node or reuse the last possible RAG node.
# The `decideDocRag` node is where the initial RAG path decision is made.
# The `retrieveEmails` node is where the email RAG path ends.
# The `retrieveDocs` node is where the doc RAG path ends.

# Let's route to the response type decision *after* any retrieval is done.

# 6a. RAG Decision Routing


def route_after_rag_decisions(state: GraphState) -> Literal["generateEmailQuery", "generateDocQuery", "decideResponseType"]:
    email_decision = state.get("email_rag_decision")
    doc_decision = state.get("doc_rag_decision")

    if email_decision == "yes":
        print("--- Routing to Email RAG ---")
        return "generateEmailQuery"
    elif doc_decision == "yes":
        print("--- Routing to Document RAG (after skipping Email RAG) ---")
        return "generateDocQuery"
    else:
        print("--- Routing directly to Response Type Decision (No RAG) ---")
        # If no RAG needed, go straight to deciding the response type
        return "decideResponseType"


workflow.add_conditional_edges(
    "decideDocRag",
    route_after_rag_decisions,
    {
        "generateEmailQuery": "generateEmailQuery",
        "generateDocQuery": "generateDocQuery",
        "decideResponseType": "decideResponseType"  # New target if skipping RAG
    }
)

# 6b. Routing after Email RAG


def route_after_email_rag(state: GraphState) -> Literal["generateDocQuery", "decideResponseType"]:
    doc_decision = state.get("doc_rag_decision")
    if doc_decision == "yes":
        print("--- Routing from Email RAG to Document RAG ---")
        return "generateDocQuery"
    else:
        print("--- Routing from Email RAG to Response Type Decision ---")
        # Go to decide response type after email RAG (if no doc RAG)
        return "decideResponseType"


workflow.add_conditional_edges(
    "retrieveEmails",  # Source node after email retrieval
    route_after_email_rag,
    {
        "generateDocQuery": "generateDocQuery",
        "decideResponseType": "decideResponseType"  # New target
    }
)

# 6c. Edge after Document RAG
# Both paths (skipped email RAG -> doc RAG, or email RAG -> doc RAG) now lead here
# After retrieving docs, always decide the response type
workflow.add_edge("retrieveDocs", "decideResponseType")  # New target

# --- RESPONSE GENERATION ---

# 7. Add the Response Type Decision Node
workflow.add_node("decideResponseType", nodes.decide_response_type)
# Edges leading to this node are defined in steps 6a, 6b, 6c

# 8. Add the two final response generation nodes
# Rename original node call here
workflow.add_node("generateEmailBodyResponse",
                  nodes.generate_email_body_response)
workflow.add_node("generateChatResponse", nodes.generate_chat_response)

# 9. Conditional routing FROM the decision node


def route_to_final_generator(state: GraphState) -> Literal["generateEmailBodyResponse", "generateChatResponse"]:
    """Routes to the appropriate generator based on the decision."""
    response_type = state.get("response_type")
    if response_type == "generate_email":
        print("--- Routing to Email Body Generation ---")
        return "generateEmailBodyResponse"
    else:  # Default or 'generate_chat'
        print("--- Routing to Chat Response Generation ---")
        return "generateChatResponse"


workflow.add_conditional_edges(
    "decideResponseType",
    route_to_final_generator,
    {
        "generateEmailBodyResponse": "generateEmailBodyResponse",
        "generateChatResponse": "generateChatResponse",
    }
)

# 10. End the graph: Both final generators lead to END
workflow.add_edge("generateEmailBodyResponse", END)
workflow.add_edge("generateChatResponse", END)

# Compile the graph
app = workflow.compile(checkpointer=memory_saver)
