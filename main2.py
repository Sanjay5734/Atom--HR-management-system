from langchain_core.messages import HumanMessage, AIMessage
from typing import Optional, List
from graph import app  # app is now compiled with the checkpointer
import uuid  # To generate unique thread IDs if needed

# In-memory storage for conversation results (optional, for demonstration)
# conversation_results = {}


def run_turn(
    user_input: str,
    thread_id_message: str,  # thread_id is now mandatory for checkpointer
    thread_id_config: str,
    user_email: str,
    is_initial_message: bool,  # Flag to know if we need thread context
    is_reply: bool  # If its a reply to a mail conversation
):
    config = {"configurable": {"thread_id": thread_id_config}}

    graph_input = {"messages": [HumanMessage(content=user_input)]}

    if is_initial_message:
        graph_input["is_reply"] = is_reply
        graph_input["thread_id"] = thread_id_message
        graph_input["user_email"] = user_email

    print(f"\n--- Running Turn for Thread ID: {thread_id_config} ---")
    print(f"Input Message: {user_input}")
    if is_initial_message:
        print(
            f"Passing initial context: is_reply={graph_input.get('is_reply')}, user_email={user_email}")

    final_state_after_turn = None
    output_message = ""

    final_state_after_turn = app.invoke(graph_input, config=config)

    if final_state_after_turn and "messages" in final_state_after_turn:
        last_message = final_state_after_turn["messages"][-1]
        if isinstance(last_message, AIMessage):
            output_message = last_message.content
            print("\n--- Assistant Response ---")
            print(output_message)
        else:
            print("\n--- Error: Expected last message to be AIMessage ---")
            print(final_state_after_turn["messages"])
            output_message = "Error: Assistant did not generate a response."
    else:
        print("\n--- Error: Graph execution did not return expected state ---")
        output_message = "Error: Graph execution failed."

    return output_message, final_state_after_turn  # Return message and state


# --- Example Usage ---

# Scenario 1: Start a new conversation thread
print("****** Starting New Conversation (Thread 1) ******")
thread_1_id = f"thread_{uuid.uuid4()}"
user_email_1 = "bob.finance@examplefinance.com"
thread_1_msg = "ExpenseReportPolicyUpdate"

# First turn
response1_1, state1_1 = run_turn(
    user_input="Draft a mail to ask regarding me not being able to attend upcoming training session held on November 1st due to unforseen circumstances",
    thread_id_message=thread_1_msg,
    thread_id_config=thread_1_id,
    user_email=user_email_1,
    is_initial_message=True,
    is_reply=True
)


# Second turn (Checkpointer loads state for thread_1_id)
response1_2, state1_2 = run_turn(
    user_input="Actually, make it a bit more stern and longer.",
    thread_id_message=thread_1_msg,
    thread_id_config=thread_1_id,
    user_email=user_email_1,
    is_initial_message=False,
    is_reply=True
)
# print("-" * 20)
# # state1_2 will have messages from both turns
# print("Final State for Thread 1:", state1_2)
# print("-" * 20)


# # Scenario 2: Simulate replying to an existing email thread
# print("\n****** Replying to Existing Email (Thread 2) ******")
# # A known thread ID that might have history in ChromaDB
# thread_2_id = "thread-abc-123"
# user_email_2 = "charlie@example.com"

# # First turn for this interaction (but it's a reply context)
# response2_1, state2_1 = run_turn(
#     user_input="Thanks for the update. Can you check the company policy on travel expenses?",
#     thread_id=thread_2_id,
#     user_email=user_email_2,
#     # It's the first message *in this run*, triggering 'is_reply' logic
#     is_initial_message=True
# )

# # Second turn for this interaction
# response2_2, state2_2 = run_turn(
#     user_input="Okay, what about the per diem rates for international travel?",
#     thread_id=thread_2_id,  # Same thread_id
#     user_email=user_email_2,
#     is_initial_message=False
# )
# print("-" * 20)
# print("Final State for Thread 2:", state2_2)
# print("-" * 20)

# You can inspect the checkpointer's internal state (for debugging)
# print("\nCheckpointer internal state:", memory_saver.storage)
