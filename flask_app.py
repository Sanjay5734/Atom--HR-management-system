# app.py

import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables (like GOOGLE_API_KEY)
load_dotenv()

# Import the compiled LangGraph application
# Ensure graph.py correctly compiles the app with MemorySaver
try:
    from graph import app as langgraph_app
except ImportError:
    print("Error: Could not import 'app' from graph.py.")
    print("Ensure graph.py exists and compiles the workflow correctly.")
    exit(1)
except Exception as e:
    print(f"Error importing or compiling graph: {e}")
    exit(1)

# --- Flask App Setup ---
flask_app = Flask(__name__)
# Enable CORS for frontend interaction (adjust origins as needed for security)
CORS(flask_app)

# --- API Endpoint ---

@flask_app.route('/chat', methods=['POST'])
def chat_endpoint():
    """
    Handles chat requests, manages conversation state, and interacts
    with the LangGraph application.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        user_input = data.get('user_input')
        user_email = data.get('user_email')
        # The actual ID of the email thread (for fetching history)
        thread_id_message = data.get('thread_id_message')
        # The ID for managing the *conversation state* in LangGraph
        conversation_id = data.get('conversation_id')

        if not user_input:
            return jsonify({"error": "'user_input' is required"}), 400
        if not user_email:
            return jsonify({"error": "'user_email' is required"}), 400

        is_new_conversation = False
        if not conversation_id:
            conversation_id = f"conv_{uuid.uuid4()}" # Generate a new ID for LangGraph state
            is_new_conversation = True
            print(f"--- Starting New Conversation (ID: {conversation_id}) ---")
        else:
            print(f"--- Continuing Conversation (ID: {conversation_id}) ---")


        # --- Prepare Input for LangGraph ---

        # Configuration for the checkpointer (MemorySaver)
        # Tells LangGraph which conversation state to load/save
        config = {"configurable": {"thread_id": conversation_id}}

        # Base input: the user's message
        graph_input = {"messages": [HumanMessage(content=user_input)]}

        # If it's the *first* message for this conversation_id,
        # provide the initial context needed by the graph's starting nodes.
        if is_new_conversation:
            graph_input["user_email"] = user_email
            # Pass the email thread ID for potential history fetching
            graph_input["thread_id"] = thread_id_message
            # Determine if the context is a reply based on email thread ID presence
            graph_input["is_reply"] = bool(thread_id_message)
            print(f"Initial context: user_email={user_email}, thread_id={thread_id_message}, is_reply={graph_input['is_reply']}")

        print(f"Invoking graph for conversation {conversation_id}...")
        print(f"Input: {graph_input}")


        # --- Invoke LangGraph Application ---
        try:
            # Use invoke to get the final state after the graph runs
            final_state = langgraph_app.invoke(graph_input, config=config)

            # Extract the latest AI message from the final state
            if final_state and "messages" in final_state and final_state["messages"]:
                last_message = final_state["messages"][-1]
                if isinstance(last_message, AIMessage):
                    ai_response = last_message.content
                    print(f"--- AI Response Sent (Conversation ID: {conversation_id}) ---")
                else:
                    # This might happen if the graph ends unexpectedly
                    print(f"Warning: Last message in state is not AIMessage for {conversation_id}. State: {final_state}")
                    ai_response = "Assistant finished processing, but no standard response was generated."
            else:
                print(f"Error: Graph did not return expected final state for {conversation_id}. State: {final_state}")
                ai_response = "Error: Could not retrieve response from assistant."
                return jsonify({"error": "Graph execution failed to produce a final state.", "conversation_id": conversation_id}), 500

        except Exception as e:
            print(f"Error during LangGraph invocation for {conversation_id}: {e}")
            # Consider more specific error logging or reporting here
            return jsonify({"error": f"An error occurred processing your request: {e}", "conversation_id": conversation_id}), 500


        # --- Return Response ---
        return jsonify({
            "response": ai_response,
            "conversation_id": conversation_id # Return the ID for the client to use in the next request
        })

    except Exception as e:
        print(f"Unhandled exception in /chat endpoint: {e}")
        # Generic server error
        return jsonify({"error": "An internal server error occurred."}), 500

# --- Run Flask App ---
if __name__ == '__main__':
    # Set debug=False for production
    flask_app.run(debug=True, host='0.0.0.0', port=5001) # Example port