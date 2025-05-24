import os
import shutil
import json
from dotenv import load_dotenv
from datetime import datetime
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from schemas import EmailSchema

load_dotenv()

persist_directory = "./db"
collection_name = "emails"

print("loading embedder")
embedder = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
print("embedder loaded")

email_store = Chroma(
    persist_directory=persist_directory,
    collection_name=collection_name,
    embedding_function=embedder
)

json_folder = "./email_source"
json_dump_folder = "./email_dumps"

# List to accumulate documents
documents = []

# Iterate over each JSON file in the directory
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(json_folder, filename)
        with open(file_path, "r") as f:
            # Each file contains a list of message dictionaries
            messages = json.load(f)
            for message in messages:
                try:
                    # Validate and parse the message using EmailSchema
                    email = EmailSchema.model_validate(message)
                    # Convert the validated email to a dictionary
                    metadata = email.model_dump(by_alias=True)
                    metadata.pop("body", None)

                    # Create a Document with the email body and metadata
                    doc = Document(page_content=email.body, metadata=metadata)
                    documents.append(doc)
                except Exception as e:
                    print(f"Error parsing message in {filename}: {e}")
    shutil.move(os.path.join(json_folder, filename), json_dump_folder)

# Save permanently
email_store.add_documents(documents)

print(f"Stored {len(documents)} email documents in the Chroma DB.")
