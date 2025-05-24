from typing import Annotated
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import ToolMessage, HumanMessage, AIMessage
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_community.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

# ========== Embedding and Vector Stores ==========
persist_directory = "./db"
doc_store_name = "documents"
email_store_name = "emails"

embedder = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

doc_store = Chroma(
    persist_directory=persist_directory,
    collection_name=doc_store_name,
    embedding_function=embedder
)

email_store = Chroma(
    persist_directory=persist_directory,
    collection_name=email_store_name,
    embedding_function=embedder
)

# ========== Tools ==========
@tool(response_format="content_and_artifact")
def retrieve_docs(query: str):
    """Retrieve any information from company documents based on user query"""
    retrieved_docs = doc_store.similarity_search(query, k=3)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

@tool(response_format="content_and_artifact")
def retrieve_emails(query: str):
    """Retrieve any information from stored emails based on user query"""
    retrieved_docs = email_store.similarity_search(query, k=4)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

retriever_tools = [retrieve_docs, retrieve_emails]
retrievers_name_dict = {t.name: t for t in retriever_tools}

# ========== LLM ==========
llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash")
llm_with_tools = llm.bind_tools(retriever_tools)

# ========== State Definition ==========
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ========== Logic Functions ==========
def validate_retrievers_calls(state: State):
    ai_message = state["messages"][-1]
    if not len(ai_message.tool_calls) > 0:
        return END

    allowed_tools = [t.name for t in retriever_tools]
    invalid_tools = [tc['name'] for tc in ai_message.tool_calls
                     if tc["name"] not in allowed_tools]

    # Uncomment to handle invalid tools via error node
    # if invalid_tools:
    #     state["invalid_tools"] = invalid_tools
    #     return "error_handling"

    return "execute_tools"

def execute_retrievers(state: State):
    tool_calls = state['messages'][-1].tool_calls
    results = []

    for t in tool_calls:
        if t['name'] not in retrievers_name_dict:
            result = "Error: No such tool found."
        else:
            result = retrievers_name_dict[t['name']].invoke(t['args'])

        results.append(
            ToolMessage(
                tool_call_id=t['id'],
                name=t['name'],
                content=str(result)
            )
        )
    return {'messages': results}

def generate_text(state: State):
    result = llm_with_tools.invoke(state["messages"])
    return {"messages": [result]}

def error_handling(state: State):
    invalid_tools = state.get("invalid_tools", [])
    allowed_tools = [t.name for t in retriever_tools]
    error_message = f"Error: The following tools are not valid: {', '.join(invalid_tools)}. "
    error_message += f"Available tools are: {', '.join(allowed_tools)}"

    feedback_message = AIMessage(content=error_message)
    if hasattr(state, "invalid_tools"):
        del state.invalid_tools

    return {'messages': [feedback_message]}

# ========== LangGraph Workflow ==========
workflow = StateGraph(State)

workflow.add_node("generate_text", generate_text)
workflow.add_node("execute_retrievers", execute_retrievers)
workflow.add_node("error_handling", error_handling)

workflow.add_edge(START, "generate_text")
workflow.add_conditional_edges(
    "generate_text",
    validate_retrievers_calls,
    {
        "execute_tools": "execute_retrievers",
        # "error_handler": "error_handling",
        END: END
    }
)
workflow.add_edge("execute_retrievers", "generate_text")
# workflow.add_edge("error_handling", "generate_text")

# ========== Final Graph ==========
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
