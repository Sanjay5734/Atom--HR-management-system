# schemas.py
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Annotated
from typing import List, Literal, Optional
from langgraph.graph.message import add_messages
from langchain_core.documents import Document  # Import Document


class EmailSchema(BaseModel):
    threadId: str = Field(description="ID for conversation thread")
    messageId: str = Field(description="message ID")
    to: str = Field(description="reciever mail id")
    from_: str = Field(description="sender mail id",
                       alias="from")  # alias is good
    subject: str = Field(description="subject of the mail")
    body: str = Field(description="body of the mail")
    date: str = Field(description="date in DD/MM/YYYY format")
    time: str = Field(description="time in 24 HR format HH:MM")

    class Config:
        validate_by_name = True  # Keep this if using alias
        # Pydantic v2 uses populate_by_name
        # populate_by_name = True


class GraphState(TypedDict):
    # Essential state
    # Stores the conversation history (HumanMessage, AIMessage)
    messages: Annotated[list, add_messages]
    user_query: str  # Stores the *current* user input for this turn

    # Context potentially fetched at the start of a turn
    # Use Optional for clarity, might not be present for new emails
    thread_id: Optional[str]
    user_email: str  # The email address of the user using the assistant
    is_reply: bool  # Flag to indicate if we should fetch thread history

    # Context retrieved during the graph execution
    # Formatted string of the email thread history
    thread_history_str: Optional[str]
    retrieved_emails: Optional[List[Document]]  # Emails retrieved via RAG
    retrieved_docs: Optional[List[Document]]  # Docs retrieved via RAG

    # Intermediate state (optional but can be useful for debugging)
    email_rag_decision: Optional[Literal["yes", "no"]]
    doc_rag_decision: Optional[Literal["yes", "no"]]
    generated_email_query: Optional[str]
    generated_doc_query: Optional[str]
    response_type: Optional[Literal["generate_email", "generate_chat"]]

# --- Output Schemas for Agents ---


class ResponseTypeDecision(BaseModel):
    response_type: Literal["generate_email", "generate_chat"] = Field(
        description="The type of response required: 'generate_email' for drafting email content, 'generate_chat' for a direct conversational reply."
    )


class EmailRagReqd(BaseModel):
    decision: Literal["yes", "no"] = Field(
        description="Decide whether you need to fetch PAST EMAILS (beyond the current thread) to answer user query. Say 'yes' or 'no' only")


class EmailQueryOutput(BaseModel):
    query: str = Field(
        description="The search query to find relevant past emails.")


class DocRagReqd(BaseModel):
    decision: Literal["yes", "no"] = Field(
        description="Decide whether you need to fetch relevant COMPANY DOCUMENTS to answer user query. Say 'yes' or 'no' only")


class DocQueryOutput(BaseModel):
    query: str = Field(
        description="The search query to find relevant company documents.")


class EmailWriterOutput(BaseModel):
    generated_email_body: str = Field(
        description="The generated body of the email response.")  # More specific name
