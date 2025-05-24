import os
import shutil
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


SOURCE_DIR = "source"
DUMP_DIR = "dump"
DB_DIR = "db" 


os.makedirs(DUMP_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)


vectorstore = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embedding_model
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

for filename in os.listdir(SOURCE_DIR):
    if filename.endswith(".txt"):
        filepath = os.path.join(SOURCE_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        
        chunks = text_splitter.create_documents([content], metadatas=[{"source": filename}])

       
        vectorstore.add_documents(chunks)
        print(f"✅ Split and embedded: {filename} ({len(chunks)} chunks)")

        
        shutil.move(filepath, os.path.join(DUMP_DIR, filename))


vectorstore.persist()

print("🎉 All documents split, embedded, and stored in 'db' folder using Chroma + Gemini.")

