import os
import shutil
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()


SOURCE_DIR = "./text_source"
DUMP_DIR = "./text_dumps"
DB_DIR = "./db"

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004")

collection_name = "documents"
vectorstore = Chroma(
    persist_directory=DB_DIR,
    collection_name=collection_name,
    embedding_function=embedding_model
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

for filename in os.listdir(SOURCE_DIR):
    if filename.endswith(".txt"):
        filepath = os.path.join(SOURCE_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = text_splitter.create_documents(
            [content], metadatas=[{"source": filename}])

        vectorstore.add_documents(chunks)
        print(f"Split and embedded: {filename} ({len(chunks)} chunks)")

        shutil.move(os.path.join(SOURCE_DIR, filename), DUMP_DIR)


print("All documents split, embedded, and stored in 'db' folder using Chroma + Gemini.")
