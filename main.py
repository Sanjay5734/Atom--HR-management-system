from langchain_core.messages import HumanMessage
from typing import Optional
from schemas import GraphState
from graph import app


def run_assistant(user_input: str, thread_id: Optional[str] = None, user_email: str = "user@example.com"):
    is_reply = bool(thread_id)
    # Initialise the graph state.
    initial_state = GraphState(
        messages=[HumanMessage(content=user_input)],
        user_query="",  # Will be populated by the first node
        thread_id=thread_id,
        user_email=user_email,
        is_reply=is_reply,
        thread_history_str=None,
        retrieved_emails=None,
        retrieved_docs=None,
        email_rag_decision=None,
        doc_rag_decision=None,
        generated_email_query=None,
        generated_doc_query=None
    )

    # Stream or invoke the graph
    # Using stream provides intermediate steps
    print("\n--- Running Graph ---")
    final_state = None
    for output in app.stream(initial_state, {"recursion_limit": 15}):
        # output is a dictionary where keys are node names
        # and values are the dictionary returned by that node's function
        # print(f"Output from node '{list(output.keys())[0]}':")
        print(output)  # Print the full output if needed for debugging
        # The final state is implicitly updated by LangGraph
        # Keep track of the latest full state if needed after the loop
        # final_state = app.get_state(output['__end__']...) # Check LangGraph docs for getting state post-run

    # To get the final state after streaming, you might need to manage checkpoints
    # or use invoke which returns the final state directly.
    # Example using invoke (simpler for getting final state):
    # final_state_invoke = app.invoke(initial_state, {"recursion_limit": 15})
    # final_message = final_state_invoke["messages"][-1].content
    # print("\n--- Final Generated Email ---")
    # print(final_message)
    # return final_message


# Example Calls
run_assistant("Can you tell me about travel expense policy, it's under the Finance & Compliance section",
              thread_id="thread-123")
# run_assistant("What's the company policy on remote work?", user_email="employee@company.com")
