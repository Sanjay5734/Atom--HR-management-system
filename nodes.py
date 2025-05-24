# nodes.py
from agents import Agents
from schemas import *  # Import updated schemas
from langchain_core.messages import HumanMessage, AIMessage
from schemas import *
from prompts import *


class Nodes:
    def __init__(self):
        self.agents = Agents()

    def get_user_query(self, state: GraphState) -> dict:
        """Extracts the latest human message as the user_query."""
        last_message = state["messages"][-1]
        if isinstance(last_message, HumanMessage):
            # Return the update for the state
            return {"user_query": last_message.content}
        else:
            # Should ideally not happen if inputs alternate correctly
            print("Warning: Last message was not a HumanMessage.")
            return {"user_query": ""}  # Or raise an error

    def decide_response_type(self, state: GraphState) -> dict:
        """Decides whether to generate an email body or a chat response."""
        print("--- Deciding Response Type ---")
        chat_history_str = self.agents.format_chat_history(
            state['messages'][:-1])
        user_query = state['user_query']

        # Ensure user_query is not empty (might happen in edge cases)
        if not user_query:
            print(
                "Warning: User query is empty in decide_response_type. Defaulting to chat.")
            # Defaulting to chat seems safer than email if query is missing
            return {"response_type": "generate_chat"}

        # Handle potential errors during LLM invocation
        try:
            decision_result = self.agents.response_type_agent.invoke({
                "user_query": user_query,
                "chat_history_str": chat_history_str
            })
            decision = decision_result.response_type
            print(f"Response type decision: {decision}")
            return {"response_type": decision}
        except Exception as e:
            print(f"Error deciding response type: {e}. Defaulting to chat.")
            # Fallback to chat on error
            return {"response_type": "generate_chat"}

    def check_if_reply(self, state: GraphState) -> dict:
        """Fetches and formats thread history if is_reply is True."""
        thread_history_str = None
        if state.get("is_reply") and state.get("thread_id"):
            thread_id = state["thread_id"]
            print(f"--- Fetching history for thread: {thread_id} ---")
            thread_emails = self.agents.fetch_thread_history(thread_id)
            if thread_emails:
                thread_history_str = self.agents.format_retrieved_docs(
                    thread_emails, "Email Thread History")
            else:
                thread_history_str = "No prior emails found in this thread."
            # Clear the flag after processing
            return {"thread_history_str": thread_history_str, "is_reply": False}
        else:
            # Not a reply or no thread_id provided
            return {"thread_history_str": "This is a new email thread.", "is_reply": False}

    def decide_email_rag(self, state: GraphState) -> dict:
        """Decides if past email retrieval is needed."""
        print("--- Deciding on Email RAG ---")
        chat_history_str = self.agents.format_chat_history(
            state['messages'][:-1])  # Exclude current query
        user_query = state['user_query']

        result = self.agents.rag_email_reqd_agent.invoke({
            "user_query": user_query,
            "chat_history_str": chat_history_str
        })
        print(f"Email RAG decision: {result.decision}")
        return {"email_rag_decision": result.decision}

    def decide_doc_rag(self, state: GraphState) -> dict:
        """Decides if document retrieval is needed."""
        print("--- Deciding on Document RAG ---")
        chat_history_str = self.agents.format_chat_history(
            state['messages'][:-1])
        user_query = state['user_query']

        result = self.agents.rag_doc_reqd_agent.invoke({
            "user_query": user_query,
            "chat_history_str": chat_history_str
        })
        print(f"Document RAG decision: {result.decision}")
        return {"doc_rag_decision": result.decision}

    def generate_email_query(self, state: GraphState) -> dict:
        """Generates the query for email retrieval."""
        print("--- Generating Email RAG Query ---")
        chat_history_str = self.agents.format_chat_history(
            state['messages'][:-1])
        user_query = state['user_query']

        email_query_result = self.agents.generate_email_query_agent.invoke({
            "user_query": user_query,
            "chat_history_str": chat_history_str
        })
        query = email_query_result.query
        print(f"Generated Email Query: {query}")
        return {"generated_email_query": query}

    def retrieve_emails(self, state: GraphState) -> dict:
        """Retrieves emails using the generated query."""
        print("--- Retrieving Emails ---")
        query = state.get("generated_email_query")
        if not query:
            print("Warning: No email query generated.")
            return {"retrieved_emails": None}

        retrieved_emails = self.agents.email_retriever.invoke(query)
        print(f"Retrieved {len(retrieved_emails)} emails.")
        return {"retrieved_emails": retrieved_emails}

    def generate_doc_query(self, state: GraphState) -> dict:
        """Generates the query for document retrieval."""
        print("--- Generating Document RAG Query ---")
        chat_history_str = self.agents.format_chat_history(
            state['messages'][:-1])
        user_query = state['user_query']

        doc_query_result = self.agents.generate_doc_query_agent.invoke({
            "user_query": user_query,
            "chat_history_str": chat_history_str
        })
        query = doc_query_result.query
        print(f"Generated Document Query: {query}")
        return {"generated_doc_query": query}

    def retrieve_docs(self, state: GraphState) -> dict:
        """Retrieves documents using the generated query."""
        print("--- Retrieving Documents ---")
        query = state.get("generated_doc_query")
        if not query:
            print("Warning: No document query generated.")
            return {"retrieved_docs": None}

        retrieved_docs = self.agents.doc_retriever.invoke(query)
        print(f"Retrieved {len(retrieved_docs)} documents.")
        return {"retrieved_docs": retrieved_docs}

    def generate_chat_response(self, state: GraphState) -> dict:
        """Generates a direct conversational response."""
        print("--- Generating Chat Response ---")
        user_query = state['user_query']
        # History before current query
        history_messages = state.get('messages', [])[:-1]

        # Combine available context into a single string for the chat agent
        # (Similar to email writer, but maybe less verbose)
        context_parts = []
        if state.get('thread_history_str'):
            context_parts.append(
                f"Email Thread:\n{state['thread_history_str']}")
        if state.get('retrieved_emails'):
            formatted_emails = self.agents.format_retrieved_docs(
                state['retrieved_emails'], "Past Emails")
            context_parts.append(f"Retrieved Past Emails:\n{formatted_emails}")
        if state.get('retrieved_docs'):
            formatted_docs = self.agents.format_retrieved_docs(
                state['retrieved_docs'], "Company Docs")
            context_parts.append(f"Retrieved Company Docs:\n{formatted_docs}")

        context_str = "\n\n".join(
            context_parts) if context_parts else "No additional context available."

        # Prepare input for the chat agent
        invoke_input = {
            "messages": history_messages,
            "context_str": context_str,
            "user_query": user_query,
        }

        try:
            response = self.agents.chat_agent.invoke(invoke_input)
            # Assuming chat_agent returns a AIMessage or just content string
            chat_content = response.content if hasattr(
                response, 'content') else str(response)

            # Basic check for empty response
            if not chat_content.strip():
                print(
                    "Warning: Chat agent returned an empty response. Providing fallback.")
                chat_content = "I'm ready to help. What would you like to do?"  # Generic fallback

            return {"messages": [AIMessage(content=chat_content)]}
        except Exception as e:
            print(f"Error during chat generation: {e}")
            error_message = f"Sorry, I encountered an error while generating the chat response: {e}"
            return {"messages": [AIMessage(content=error_message)]}

    def generate_email_body_response(self, state: GraphState) -> dict:
        """Generates the final email response using all context."""
        print("--- Generating Email Response ---")

        # Prepare context variables directly from the state
        user_query = state['user_query']
        # History *before* the current user query (for MessagesPlaceholder)
        # Ensure messages is a list, default to empty if not found
        history_messages = state.get('messages', [])[:-1]
        user_email = state['user_email']

        # Use the fetched thread history string, provide a default if missing
        thread_history = state.get(
            'thread_history_str', 'No thread history available.')

        # Format retrieved documents, provide defaults if missing or empty
        formatted_emails = self.agents.format_retrieved_docs(
            state.get('retrieved_emails'), "Relevant Past Emails")  # Adjusted title
        formatted_docs = self.agents.format_retrieved_docs(
            state.get('retrieved_docs'), "Relevant Company Documents")  # Adjusted title

        if not user_query:
            print("Error: Cannot generate response without user_query.")
            # Return a placeholder error message or handle appropriately
            return {"messages": [AIMessage(content="I apologize, but I couldn't process your request properly as the query was missing.")]}

        # *** The Fix: Create the input dictionary with all expected keys ***
        invoke_input = {
            "messages": history_messages,         # For MessagesPlaceholder
            "user_email": user_email,             # For system prompt
            "user_query": user_query,             # For user template
            "thread_history": thread_history,     # For user template
            "retrieved_emails": formatted_emails,  # For user template
            "retrieved_docs": formatted_docs      # For user template
        }

        # Invoke the writer agent with the complete input dictionary
        try:
            response = self.agents.email_writer_agent.invoke(invoke_input)
            generated_body = response.generated_email_body

            # Return the AI message to be added to the state's messages list
            # LangGraph's add_messages will handle appending this
            return {"messages": [AIMessage(content=generated_body)]}
        except Exception as e:
            print(f"Error during email generation: {e}")
            # Provide a fallback response in case of error
            error_message = f"Sorry, I encountered an error while generating the email response: {e}"
            return {"messages": [AIMessage(content=error_message)]}
