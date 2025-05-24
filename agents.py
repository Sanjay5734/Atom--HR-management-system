# agents.py
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.documents import Document
from typing import List, Optional
from datetime import datetime
from prompts import *
from schemas import *
from dotenv import load_dotenv
load_dotenv()


class Agents():
    def __init__(self):
        # Initialize the agent with the model and retrievers.
        # Using a slightly newer model often helps
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash")
        self.embedder = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004")
        persist_directory = "./db"
        doc_store_name = "documents"
        email_store_name = "emails"
        doc_store = Chroma(
            persist_directory=persist_directory,
            collection_name=doc_store_name,
            embedding_function=self.embedder
        )
        email_store = Chroma(
            persist_directory=persist_directory,
            collection_name=email_store_name,
            embedding_function=self.embedder
        )
        # Increase k for more context potentially, adjust as needed
        self.doc_retriever = doc_store.as_retriever(search_kwargs={"k": 5})
        self.email_retriever = email_store.as_retriever(search_kwargs={"k": 7})

        # --- Agent Definitions ---

        # RAG Decision Agents
        rag_email_reqd_prompt = PromptTemplate.from_template(
            template=RAG_EMAIL_REQD_PROMPT,
        )
        self.rag_email_reqd_agent = (
            rag_email_reqd_prompt | self.llm.with_structured_output(
                EmailRagReqd
            )
        )

        rag_doc_reqd_prompt = PromptTemplate.from_template(
            template=RAG_DOC_REQD_PROMPT,
        )
        self.rag_doc_reqd_agent = (
            rag_doc_reqd_prompt | self.llm.with_structured_output(DocRagReqd)
        )

        # Query Generation Agents
        generate_email_query_prompt = PromptTemplate.from_template(
            template=EMAIL_QUERY_GENERATION_PROMPT,
        )
        self.generate_email_query_agent = (
            generate_email_query_prompt | self.llm.with_structured_output(
                EmailQueryOutput
            )
        )

        generate_doc_query_prompt = PromptTemplate.from_template(
            template=DOC_QUERY_GENERATION_PROMPT,
        )
        self.generate_doc_query_agent = (
            generate_doc_query_prompt | self.llm.with_structured_output(
                DocQueryOutput
            )
        )

        # Email Writing Agent
        writer_agent_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", EMAIL_WRITER_SYSTEM_PROMPT),
                # Existing chat history
                MessagesPlaceholder(variable_name="messages"),
                # We will inject context here before calling the agent
                ("user", EMAIL_WRITER_USER_TEMPLATE)
            ]
        )
        self.email_writer_agent = (
            writer_agent_prompt | self.llm.with_structured_output(
                EmailWriterOutput
            )
        )
        # --- Response Type Router Agent ---
        response_type_prompt = PromptTemplate.from_template(
            template=RESPONSE_TYPE_PROMPT,
        )
        self.response_type_agent = (
            response_type_prompt | self.llm.with_structured_output(
                ResponseTypeDecision
            )
        )

        # --- Basic Chat Agent ---
        chat_agent_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", CHAT_AGENT_SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="messages"),
                ("user", CHAT_AGENT_USER_TEMPLATE)
            ]
        )
        self.chat_agent = chat_agent_prompt | self.llm

    # --- Helper Function for Retrieval ---
    # (Moved from Agents class in original code, keep it here or move to utils)
    def fetch_thread_history(self, thread_id: str) -> List[Document]:
        """Fetches and sorts emails for a given thread ID."""
        if not thread_id:
            return []
        try:
            thread_emails = self.email_retriever.invoke(
                "",
                filter={"threadId": thread_id}
            )
            # Adapt based on actual Chroma return structure

            # If direct filter doesn't work, fallback to similarity search + filtering
            # This is less efficient if the DB is large
            # thread_emails = self.email_retriever.vectorstore.similarity_search(
            #     " ", # Empty query to get all within filter scope
            #     k=100, # Adjust K high enough
            #     filter={"threadId": thread_id}
            # )

            # Simplified sorting assuming 'date' and 'time' are in metadata
            def get_datetime_key(doc):
                metadata = doc.metadata
                date_str = metadata.get("date", "")
                # Default time if missing
                time_str = metadata.get("time", "00:00")
                try:
                    # Ensure correct parsing format
                    return datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
                except ValueError:
                    print(
                        f"Warning: Could not parse date/time: {date_str} {time_str}")
                    return datetime.min  # Put unparseable dates first

            # Ensure thread_emails is a list of Document objects if using .get()
            # You might need to reconstruct Document objects if .get() returns raw dicts
            # Example reconstruction (adapt based on Chroma's actual return):
            # reconstructed_emails = [Document(page_content=d.get('page_content', ''), metadata=d.get('metadata', {})) for d in thread_emails]

            # Use reconstructed_emails if needed
            sorted_thread_emails = sorted(thread_emails, key=get_datetime_key)
            return sorted_thread_emails

        except Exception as e:
            print(f"Error fetching thread history for {thread_id}: {e}")
            return []

    # --- Helper to Format Chat History ---
    def format_chat_history(self, messages: List) -> str:
        """Formats Langchain message history into a simple string."""
        if not messages:
            return "No previous conversation history."
        history_str = ""
        for msg in messages:
            if isinstance(msg, HumanMessage):
                history_str += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                history_str += f"Assistant: {msg.content}\n"
            else:  # Handle other message types if necessary
                history_str += f"{type(msg).__name__}: {msg.content}\n"
        return history_str.strip()

    # --- Helper to Format Retrieved Documents ---
    def format_retrieved_docs(self, docs: Optional[List[Document]], title: str) -> str:
        """Formats retrieved documents into a string for the prompt."""
        if not docs:
            return f"No relevant {title} found."

        formatted = f"--- Relevant {title} Start ---\n"
        for i, doc in enumerate(docs):
            # Include relevant metadata
            metadata_str = ", ".join(
                f"{k}: {v}" for k, v in doc.metadata.items() if v)
            formatted += f"Context {i+1}:\n"
            if metadata_str:
                formatted += f"  Metadata: {metadata_str}\n"
            formatted += f"  Content: {doc.page_content}\n\n"
        formatted += f"--- Relevant {title} End ---"
        return formatted
